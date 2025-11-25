# Contributing to Auto Download Organizer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in Issues
- Use the bug report template
- Include detailed reproduction steps
- Provide system information (OS, Python version)

### Suggesting Features

- Check if the feature has been suggested before
- Clearly describe the feature and its benefits
- Consider implementation complexity

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Write clean, documented code
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation
7. Submit PR with clear description

## Development Setup

```powershell
git clone https://github.com/Adrmicc/auto-download-organizer.git
cd auto-download-organizer
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Code Standards

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Maximum line length: 100 characters
- Use meaningful variable names

## Testing

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_file_organizer.py -v
```

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move file..." not "Moves file...")
- First line: brief summary (50 chars or less)
- Detailed description in body if needed

Example:
```
Add date-based folder organization

Implements optional date-based subdirectory creation
for better file organization by time periods.
```

## Questions?

Feel free to open an issue for any questions or concerns.
