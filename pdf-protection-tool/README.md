# 🔒 PDF Protection Tool

A lightweight, cross-platform command-line tool to **password-protect PDF files** using Python. Built with [`pypdf`](https://pypi.org/project/pypdf/), it supports separate user and owner passwords, robust error handling, and clean terminal output — making it easy to secure confidential documents in seconds.

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Examples](#-examples)
- [Project Structure](#-project-structure)
- [Running Tests](#-running-tests)
- [Key Concepts](#-key-concepts)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 Password protection | Encrypts any PDF with AES-based encryption |
| 👤 Dual passwords | Separate **user** password (view) and **owner** password (edit/print) |
| 🛡️ Input validation | Checks file existence, extension, size, and password strength |
| 📋 Rich feedback | Shows page count and file sizes after encryption |
| 🚫 Error handling | Graceful messages for missing files, bad paths, and corrupt PDFs |
| 🔇 Quiet mode | `--quiet` flag for use in scripts and automation |
| 🐍 Pure Python | No external binaries required |

---

## 🎬 Demo

```
$ python pdf_protect.py financial_report.pdf secure_report.pdf MyP@ssw0rd

✅  PDF successfully protected!

   Input  : /home/user/financial_report.pdf  (245.3 KB)
   Output : /home/user/secure_report.pdf  (247.1 KB)
   Pages  : 12

   Open the output file and enter your password to verify.
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/pdf-protection-tool.git
cd pdf-protection-tool

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

```
usage: pdf_protect [-h] [--owner-password OWNER_PWD] [--quiet] [--version]
                   input output password

positional arguments:
  input                       Path to the input PDF file.
  output                      Path for the output (protected) PDF file.
  password                    Password to protect the PDF.

optional arguments:
  --owner-password OWNER_PWD  Owner password (editing/printing rights).
                              Defaults to the user password if not set.
  --quiet, -q                 Suppress all output messages.
  --version, -v               Show version and exit.
  -h, --help                  Show this help message and exit.
```

---

## 📚 Examples

**Basic — protect with a single password:**
```bash
python pdf_protect.py input.pdf protected.pdf MySecretPass
```

**Separate user and owner passwords:**
```bash
python pdf_protect.py input.pdf protected.pdf ViewOnly123 --owner-password AdminFull456
```

**Quiet mode (for use in shell scripts):**
```bash
python pdf_protect.py report.pdf secure_report.pdf secret --quiet
echo "Exit code: $?"
```

**Protect all PDFs in a folder (bash):**
```bash
for f in docs/*.pdf; do
    python pdf_protect.py "$f" "protected_$(basename "$f")" "MyP@ss"
done
```

---

## 📁 Project Structure

```
pdf-protection-tool/
│
├── pdf_protect.py          # Main CLI script
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Dev/test dependencies
├── .gitignore
├── LICENSE
└── tests/
    └── test_pdf_protect.py # Pytest test suite
```

---

## 🧪 Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=pdf_protect --cov-report=term-missing
```

---

## 🔑 Key Concepts

**File Handling** — The tool reads the source PDF page-by-page using `PdfReader` and writes each page into a new `PdfWriter` object, preserving all content and metadata.

**Encryption** — The `PdfWriter.encrypt()` method applies AES-128 encryption. A *user password* restricts opening, while an optional *owner password* restricts editing and printing.

**Command-Line Arguments** — Python's `argparse` module parses positional arguments (`input`, `output`, `password`) and optional flags (`--owner-password`, `--quiet`).

**Exception Handling** — Every stage (file validation, reading, writing) is wrapped in specific exception types (`FileNotFoundError`, `ValueError`, `PermissionError`, `IOError`) so users receive clear, actionable error messages.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please make sure all tests pass before submitting a PR.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

> Built with [Inlighn Tech]

