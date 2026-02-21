"""
Unit tests for pdf_protect.py
Run with: pytest tests/test_pdf_protect.py -v
"""

import os
import sys
import pytest
from pathlib import Path

# Make sure the parent directory is on the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_protect import validate_input_file, validate_output_path, validate_password, protect_pdf

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_pdf(tmp_path):
    """Create a minimal valid PDF for testing."""
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        pdf_path = tmp_path / "sample.pdf"
        c = rl_canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, "Test PDF — PDF Protection Tool")
        c.save()
        return pdf_path
    except ImportError:
        # Fallback: create a minimal PDF manually
        pdf_path = tmp_path / "sample.pdf"
        minimal_pdf = (
            b"%PDF-1.4\n"
            b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
            b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
            b"xref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n"
            b"0000000058 00000 n \n0000000115 00000 n \n"
            b"trailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n190\n%%EOF"
        )
        pdf_path.write_bytes(minimal_pdf)
        return pdf_path


@pytest.fixture
def output_pdf(tmp_path):
    return tmp_path / "output.pdf"


# ---------------------------------------------------------------------------
# validate_input_file
# ---------------------------------------------------------------------------

class TestValidateInputFile:
    def test_valid_pdf(self, sample_pdf):
        result = validate_input_file(str(sample_pdf))
        assert result == sample_pdf

    def test_missing_file(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="not found"):
            validate_input_file(str(tmp_path / "nonexistent.pdf"))

    def test_wrong_extension(self, tmp_path):
        txt_file = tmp_path / "document.txt"
        txt_file.write_text("hello")
        with pytest.raises(ValueError, match=".pdf extension"):
            validate_input_file(str(txt_file))

    def test_empty_file(self, tmp_path):
        empty = tmp_path / "empty.pdf"
        empty.write_bytes(b"")
        with pytest.raises(ValueError, match="empty"):
            validate_input_file(str(empty))


# ---------------------------------------------------------------------------
# validate_output_path
# ---------------------------------------------------------------------------

class TestValidateOutputPath:
    def test_valid_output_path(self, tmp_path):
        out = tmp_path / "out.pdf"
        result = validate_output_path(str(out))
        assert result == out

    def test_wrong_extension(self, tmp_path):
        with pytest.raises(ValueError, match=".pdf extension"):
            validate_output_path(str(tmp_path / "output.docx"))

    def test_nonexistent_directory(self):
        with pytest.raises(FileNotFoundError, match="directory does not exist"):
            validate_output_path("/nonexistent_dir/output.pdf")


# ---------------------------------------------------------------------------
# validate_password
# ---------------------------------------------------------------------------

class TestValidatePassword:
    def test_valid_password(self):
        validate_password("SecurePass123!")  # should not raise

    def test_empty_password(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_password("")

    def test_too_short_password(self):
        with pytest.raises(ValueError, match="at least 4 characters"):
            validate_password("abc")

    def test_minimum_length_password(self):
        validate_password("abcd")  # exactly 4 chars — should pass


# ---------------------------------------------------------------------------
# protect_pdf (integration)
# ---------------------------------------------------------------------------

class TestProtectPdf:
    def test_basic_protection(self, sample_pdf, output_pdf):
        result = protect_pdf(str(sample_pdf), str(output_pdf), "TestPass123")
        assert output_pdf.exists()
        assert result["pages_protected"] >= 1
        assert result["output_size_kb"] > 0

    def test_output_is_encrypted(self, sample_pdf, output_pdf):
        protect_pdf(str(sample_pdf), str(output_pdf), "TestPass123")
        from pypdf import PdfReader
        reader = PdfReader(str(output_pdf))
        assert reader.is_encrypted

    def test_separate_owner_password(self, sample_pdf, output_pdf):
        result = protect_pdf(
            str(sample_pdf), str(output_pdf),
            user_password="UserPass1",
            owner_password="OwnerPass1"
        )
        assert output_pdf.exists()
        assert result["pages_protected"] >= 1

    def test_missing_input_raises(self, tmp_path, output_pdf):
        with pytest.raises(FileNotFoundError):
            protect_pdf(str(tmp_path / "missing.pdf"), str(output_pdf), "pass1234")

    def test_empty_password_raises(self, sample_pdf, output_pdf):
        with pytest.raises(ValueError, match="cannot be empty"):
            protect_pdf(str(sample_pdf), str(output_pdf), "")

    def test_result_dict_keys(self, sample_pdf, output_pdf):
        result = protect_pdf(str(sample_pdf), str(output_pdf), "SomePass!")
        expected_keys = {"input_file", "output_file", "pages_protected",
                         "input_size_kb", "output_size_kb"}
        assert expected_keys.issubset(result.keys())
