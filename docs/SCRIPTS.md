# PowerShell scripts for common tasks

## Setup and Installation

### Initial Setup
```powershell
# Run the setup script
python setup_project.py
```

### Manual Setup
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Development Commands

### Running Tests
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_file_organizer.py

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

### Code Quality
```powershell
# Check code style with flake8
flake8 src tests

# Format code with black
black src tests

# Check formatting without changing files
black --check src tests
```

### Running the Application
```powershell
# Organize Downloads folder (dry run)
python -m src.cli organize --dry-run

# Organize Downloads folder (actual)
python -m src.cli organize

# Clean duplicates (report only)
python -m src.cli clean-duplicates --report-only

# Clean duplicates (actual)
python -m src.cli clean-duplicates

# Full workflow
python -m src.cli full -d "C:\Users\$env:USERNAME\Downloads" --clean-duplicates
```

### Documentation
```powershell
# View README
Get-Content README.md

# View Quick Start
Get-Content docs\QUICKSTART.md

# View Polish instructions
Get-Content docs\INSTRUKCJA_PL.md
```

## Git Commands

### Initial Commit
```powershell
git init
git add .
git commit -m "Initial commit: Auto Download Organizer"
```

### Push to GitHub
```powershell
git remote add origin https://github.com/Adrmicc/auto-download-organizer.git
git branch -M main
git push -u origin main
```

### Regular Workflow
```powershell
# Check status
git status

# Add all changes
git add .

# Commit with message
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

### Branching
```powershell
# Create new branch
git checkout -b feature/new-feature

# Switch to branch
git checkout main

# Merge branch
git merge feature/new-feature

# Delete branch
git branch -d feature/new-feature
```

## Testing Commands

### Test Specific Modules
```powershell
# Test file organizer
pytest tests/test_file_organizer.py -v

# Test duplicate cleaner
pytest tests/test_duplicate_cleaner.py -v

# Test logger
pytest tests/test_logger.py -v

# Test config loader
pytest tests/test_config_loader.py -v
```

### Coverage Reports
```powershell
# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/

# View coverage report
Start-Process htmlcov\index.html
```

## Utility Commands

### Clean Project
```powershell
# Remove Python cache files
Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse | Remove-Item -Recurse -Force

# Remove test cache
Remove-Item -Path .pytest_cache -Recurse -Force

# Remove coverage files
Remove-Item -Path htmlcov -Recurse -Force
Remove-Item -Path .coverage -Force
```

### Create Distribution
```powershell
# Build distribution packages
python setup.py sdist bdist_wheel

# Check distribution
twine check dist/*
```

### Virtual Environment
```powershell
# Deactivate virtual environment
deactivate

# Remove virtual environment
Remove-Item -Path venv -Recurse -Force

# Recreate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Useful Aliases

Add these to your PowerShell profile for quick access:

```powershell
# Open profile
notepad $PROFILE

# Add these aliases:
function Activate-Venv { .\venv\Scripts\Activate.ps1 }
function Run-Tests { pytest -v }
function Run-Coverage { pytest --cov=src tests/ }
function Format-Code { black src tests }
function Organize-Downloads { python -m src.cli organize }

Set-Alias activate Activate-Venv
Set-Alias test Run-Tests
Set-Alias coverage Run-Coverage
Set-Alias format Format-Code
Set-Alias organize Organize-Downloads
```

## Troubleshooting

### Fix Common Issues
```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Clear pip cache
pip cache purge

# Update pip
python -m pip install --upgrade pip

# Check installed packages
pip list

# Check for outdated packages
pip list --outdated
```

### Python Path Issues
```powershell
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Add current directory to PYTHONPATH (temporary)
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"
```

## Quick Commands Summary

```powershell
# Setup
python setup_project.py

# Develop
pytest                                    # Run tests
python -m src.cli organize --dry-run     # Test run
python -m src.cli organize               # Organize files

# Git
git add .; git commit -m "message"; git push

# Clean
pytest --cov=src tests/                  # Check coverage
black src tests                          # Format code
flake8 src tests                         # Lint code
```
