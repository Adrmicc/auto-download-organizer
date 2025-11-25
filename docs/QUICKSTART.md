# Quick Start Guide

## Installation

1. **Clone the repository:**
```powershell
git clone https://github.com/Adrmicc/auto-download-organizer.git
cd auto-download-organizer
```

2. **Create virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

## Basic Usage

### 1. Preview Before Organizing (Dry Run)

```powershell
python -m src.cli organize --dry-run
```

### 2. Organize Your Downloads Folder

```powershell
python -m src.cli organize
```

This will:
- Scan your Downloads folder
- Organize files into categories (Documents, Images, Videos, etc.)
- Create a log file with all operations

This shows what would happen without making any changes.

### 3. Clean Duplicate Files

```powershell
python -m src.cli clean-duplicates --report-only
```

This shows a report of duplicate files without removing them.

To actually remove duplicates:

```powershell
python -m src.cli clean-duplicates
```

### 4. Full Organization

```powershell
python -m src.cli full -d "C:\Users\YourName\Downloads" --clean-duplicates
```

This runs both organization and duplicate cleaning in one command.

## Common Scenarios

### Organize with Date Folders

Useful for archiving:

```powershell
python -m src.cli organize --date-folders
```

Files will be organized like:
```
Downloads/
  Documents/
    2025-11/
      file1.pdf
      file2.doc
    2025-10/
      old_file.pdf
```

### Custom Configuration

1. Create your config:
```powershell
python -m src.cli create-config my_config.yaml
```

2. Edit `my_config.yaml` to customize categories

3. Use it:
```powershell
python -m src.cli organize -c my_config.yaml
```

### View Operation History

```powershell
python -m src.cli show-log
```

## Tips

- Always try `--dry-run` first to preview changes
- Check logs regularly with `show-log`
- Use `--report-only` with duplicates to see what would be removed
- Backup important files before first run
- Customize config for your specific needs

## Next Steps

- Read the full [README.md](../README.md)
- Check out [API Documentation](API.md)
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for development

## Troubleshooting

**Problem**: "Module not found" error
**Solution**: Make sure you activated the virtual environment and installed dependencies

**Problem**: Permission errors
**Solution**: Run PowerShell as Administrator or check file permissions

**Problem**: Files not being organized
**Solution**: Check if file extensions are in the config, add them if needed
