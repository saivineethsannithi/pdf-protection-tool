# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2025-01-01

### Added
- Initial release of the PDF Protection Tool.
- Command-line interface using `argparse` with positional `input`, `output`, and `password` arguments.
- Support for separate **user password** (view access) and **owner password** (full permissions).
- Input validation: file existence, `.pdf` extension check, empty file detection, password length check.
- Metadata preservation from the original PDF.
- Detection and rejection of already-encrypted input PDFs.
- `--quiet` / `-q` flag for use in scripts and pipelines.
- `--version` / `-v` flag.
- Comprehensive Pytest test suite covering all validation functions and integration scenarios.
- MIT License.
- `.gitignore` pre-configured for Python projects.
