# 📁 Auto Download Organizer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional, automated file organization tool that keeps your Downloads folder clean and organized. Features intelligent categorization, duplicate detection, and comprehensive logging.

## ✨ Features

- 🗂️ **Automatic Categorization**: Organizes files into predefined categories (Documents, Images, Videos, etc.)
- 🔍 **Duplicate Detection**: Finds and removes duplicate files based on content hash
- 📝 **Comprehensive Logging**: JSON-based logging for all operations
- 🎯 **CLI Interface**: Professional command-line interface with multiple commands
- 🔧 **Customizable**: YAML-based configuration for custom rules
- 🧪 **Dry Run Mode**: Test operations before making actual changes
- 📅 **Date Folders**: Optional date-based subdirectory organization
- 🎨 **Multiple Strategies**: Choose how to handle duplicates (newest, oldest, shortest name)

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Install from source

```powershell
# Clone the repository
git clone https://github.com/Adrmicc/auto-download-organizer.git
cd auto-download-organizer

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## 🎯 Quick Start

Organize your Downloads folder with default settings:

```powershell
python -m src.cli organize
```

Clean duplicate files:

```powershell
python -m src.cli clean-duplicates
```

Run full organization (organize + clean duplicates):

```powershell
python -m src.cli full -d "C:\Users\YourName\Downloads" --clean-duplicates
```

## 📖 Usage

### Basic Commands

#### 1. Organize Files

Organize files in a specific directory:

```powershell
python -m src.cli organize -d "C:\Users\YourName\Downloads"
```

With date-based folders:

```powershell
python -m src.cli organize -d "C:\Users\YourName\Downloads" --date-folders
```

Dry run (preview without making changes):

```powershell
python -m src.cli organize -d "C:\Users\YourName\Downloads" --dry-run
```

#### 2. Clean Duplicates

Find and remove duplicates:

```powershell
python -m src.cli clean-duplicates -d "C:\Users\YourName\Downloads"
```

Only show report without removing:

```powershell
python -m src.cli clean-duplicates -d "C:\Users\YourName\Downloads" --report-only
```

Choose which duplicate to keep:

```powershell
python -m src.cli clean-duplicates -d "C:\Users\YourName\Downloads" --keep newest
```

Options for `--keep`:
- `newest` - Keep the most recently modified file (default)
- `oldest` - Keep the oldest file
- `shortest` - Keep the file with the shortest name

#### 3. Full Organization

Run complete organization process:

```powershell
python -m src.cli full -d "C:\Users\YourName\Downloads" --clean-duplicates
```

#### 4. View Logs

Display operation history:

```powershell
python -m src.cli show-log
```

#### 5. Create Custom Configuration

Generate a default config file to customize:

```powershell
python -m src.cli create-config my_config.yaml
```

## ⚙️ Configuration

### Default File Categories

The organizer comes with predefined categories:

- **Documents**: PDF, DOC, DOCX, TXT, etc.
- **Images**: JPG, PNG, GIF, SVG, etc.
- **Videos**: MP4, AVI, MKV, MOV, etc.
- **Audio**: MP3, WAV, FLAC, AAC, etc.
- **Archives**: ZIP, RAR, 7Z, TAR, etc.
- **Programs**: EXE, MSI, DMG, etc.
- **Code**: PY, JS, HTML, CSS, etc.
- **Spreadsheets**: XLSX, XLS, CSV, etc.
- **Presentations**: PPTX, PPT, etc.
- **Ebooks**: EPUB, MOBI, AZW, etc.

### Custom Configuration

Create a custom configuration file:

```yaml
categories:
  MyDocuments:
    - .pdf
    - .doc
  MyImages:
    - .jpg
    - .png

settings:
  create_date_folders: false
  log_file: organizer_log.json
  dry_run: false
```

Use your custom config:

```powershell
python -m src.cli organize -d "C:\Users\YourName\Downloads" -c my_config.yaml
```

## 🛠️ Development

### Project Structure

```
auto-download-organizer/
├── src/
│   ├── __init__.py
│   ├── cli.py                 # CLI interface
│   ├── config_loader.py       # Configuration management
│   ├── file_organizer.py      # File organization logic
│   ├── duplicate_cleaner.py   # Duplicate detection
│   └── logger.py              # Logging system
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_file_organizer.py
│   ├── test_duplicate_cleaner.py
│   ├── test_logger.py
│   └── test_config_loader.py
├── config/
│   └── default_config.yaml
├── docs/
├── requirements.txt
├── setup.py
├── .gitignore
├── LICENSE
└── README.md
```

### Setting Up Development Environment

```powershell
# Clone and setup
git clone https://github.com/Adrmicc/auto-download-organizer.git
cd auto-download-organizer

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install development dependencies
pip install -r requirements.txt
pip install -e .
```

## 🧪 Testing

Run all tests:

```powershell
pytest
```

Run with coverage:

```powershell
pytest --cov=src tests/
```

Run specific test file:

```powershell
pytest tests/test_file_organizer.py
```

Run with verbose output:

```powershell
pytest -v
```

## 📊 Features in Detail

### Logging System

All operations are logged to a JSON file (`organizer_log.json` by default):

```json
{
  "session_start": "2025-11-25T10:00:00",
  "session_end": "2025-11-25T10:05:00",
  "total_operations": 45,
  "by_type": {
    "move": 40,
    "delete_duplicate": 5
  },
  "by_status": {
    "success": 44,
    "error": 1
  },
  "operations": [...]
}
```

### Duplicate Detection

Uses SHA256 hashing to identify duplicates based on file content, not just filename:

- Fast and reliable
- Works across different filenames
- Multiple keep strategies
- Detailed reporting

### Dry Run Mode

Test any operation before making changes:

```powershell
python -m src.cli organize -d "C:\Downloads" --dry-run
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write descriptive docstrings
- Add tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Uses [PyYAML](https://pyyaml.org/) for configuration
- Tested with [Pytest](https://pytest.org/)

## 📧 Contact

Project Link: [https://github.com/Adrmicc/auto-download-organizer](https://github.com/Adrmicc/auto-download-organizer)
---

⭐ If you find this project useful, please consider giving it a star!
