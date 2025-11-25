# FAQ - Frequently Asked Questions

## General Questions

### Q: What does this tool do?
A: Auto Download Organizer automatically organizes files in your Downloads folder by categorizing them (Documents, Images, Videos, etc.) and can also detect and remove duplicate files.

### Q: Is it safe to use?
A: Yes, but always backup important files first. Use `--dry-run` mode to preview changes before making them permanent.

### Q: What operating systems are supported?
A: Windows, macOS, and Linux. The tool is cross-platform.

### Q: Do I need programming knowledge to use it?
A: No, you can use the CLI commands. However, you can also use it programmatically if you know Python.

## Installation Questions

### Q: What Python version do I need?
A: Python 3.8 or higher is required.

### Q: Do I need to install anything besides Python?
A: Yes, install the dependencies listed in `requirements.txt` using:
```powershell
pip install -r requirements.txt
```

### Q: Should I use a virtual environment?
A: Yes, it's highly recommended to avoid dependency conflicts:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## Usage Questions

### Q: How do I organize my Downloads folder?
A: Run:
```powershell
python -m src.cli organize
```

### Q: Can I organize a different folder?
A: Yes, use the `-d` option:
```powershell
python -m src.cli organize -d "C:\Path\To\Folder"
```

### Q: What does dry run mode do?
A: It shows what would be done without actually moving or deleting files:
```powershell
python -m src.cli organize --dry-run
```

### Q: How do I find duplicate files?
A: Use:
```powershell
python -m src.cli clean-duplicates --report-only
```

### Q: How are files categorized?
A: Based on file extensions. For example:
- `.pdf`, `.doc` → Documents
- `.jpg`, `.png` → Images
- `.mp4`, `.avi` → Videos

### Q: Can I customize the categories?
A: Yes, create a custom config:
```powershell
python -m src.cli create-config my_config.yaml
```
Then edit the file and use it:
```powershell
python -m src.cli organize -c my_config.yaml
```

## Duplicate Detection Questions

### Q: How does duplicate detection work?
A: It calculates SHA256 hash of file contents. Files with identical content have the same hash, even if filenames differ.

### Q: Which duplicate is kept?
A: By default, the newest file is kept. You can change this with `--keep`:
```powershell
python -m src.cli clean-duplicates --keep oldest
```

Options: `newest`, `oldest`, `shortest`

### Q: Will it delete files with the same name but different content?
A: No, only files with identical content (same hash) are considered duplicates.

### Q: Can I undo duplicate removal?
A: No, deleted files cannot be recovered. Always use `--dry-run` first!

## Configuration Questions

### Q: Where is the configuration file?
A: Default configuration is built-in. You can create a custom one with:
```powershell
python -m src.cli create-config my_config.yaml
```

### Q: How do I add a new category?
A: Edit your config file:
```yaml
categories:
  MyCategory:
    - .ext1
    - .ext2
```

### Q: Can I exclude certain file types?
A: Files not matching any category go to "Others" folder. To skip organizing them, modify the code or use a custom config.

## Logging Questions

### Q: Where are the logs stored?
A: By default in `organizer_log.json` in the current directory.

### Q: How do I view the logs?
A: Use:
```powershell
python -m src.cli show-log
```
Or open `organizer_log.json` in any text editor.

### Q: Can I change the log file location?
A: Yes, use `--log-file` option:
```powershell
python -m src.cli organize --log-file "C:\Logs\my_log.json"
```

## Advanced Questions

### Q: Can I organize files by date?
A: Yes, use `--date-folders`:
```powershell
python -m src.cli organize --date-folders
```
This creates subdirectories like `Documents/2025-11/`

### Q: Can I schedule automatic organization?
A: Use Windows Task Scheduler or cron (Linux/Mac) to run the script periodically. See docs for examples.

### Q: Can I use this programmatically in my own script?
A: Yes! Example:
```python
from src.file_organizer import FileOrganizer
from src.logger import OrganizerLogger

logger = OrganizerLogger()
organizer = FileOrganizer("C:/Downloads", logger=logger)
organizer.organize()
```

### Q: How do I run the full workflow (organize + clean)?
A: Use:
```powershell
python -m src.cli full -d "C:\Downloads" --clean-duplicates
```

## Troubleshooting

### Q: I get "Module not found" error
A: Make sure:
1. Virtual environment is activated
2. Dependencies are installed: `pip install -r requirements.txt`
3. You're in the project directory

### Q: I get "Permission denied" error
A: Some files may be in use. Close programs that might be using files in your Downloads folder.

### Q: The CLI doesn't work
A: Make sure you're using the correct command format:
```powershell
python -m src.cli organize
```
Not just `organize`

### Q: Tests fail
A: Make sure pytest is installed:
```powershell
pip install pytest
pytest
```

### Q: How do I update the tool?
A: Pull the latest changes from GitHub:
```powershell
git pull origin main
pip install -r requirements.txt
```

## Performance Questions

### Q: How fast is it?
A: Speed depends on:
- Number of files
- File sizes (for duplicate detection)
- Disk speed

Typical Downloads folder (100-500 files) organizes in seconds.

### Q: Does it work with large files?
A: Yes, but duplicate detection is slower with very large files (GB+) since it calculates hashes.

### Q: Can I organize thousands of files?
A: Yes, the tool scales well. For very large directories, it may take longer but will complete successfully.

## Safety Questions

### Q: Will it delete my files?
A: Only duplicate files are deleted (if you use `clean-duplicates` command). Regular organization only moves files.

### Q: What if something goes wrong?
A: All operations are logged. Check `organizer_log.json` for details. Always backup important files first!

### Q: Can I undo organization?
A: There's an `undo_last_session()` method in the code, but it's safer to keep backups.

### Q: Will it modify file contents?
A: No, it only moves files to different folders. File contents are never modified.

## Contributing Questions

### Q: Can I contribute to this project?
A: Yes! See CONTRIBUTING.md for guidelines.

### Q: I found a bug, what should I do?
A: Open an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your OS and Python version

### Q: Can I suggest a new feature?
A: Absolutely! Open an issue on GitHub with your suggestion.

## Still Have Questions?

- Read the full documentation: `README.md`, `docs/QUICKSTART.md`
- Check examples: `docs/examples.py`
- Open an issue on GitHub
- Read the API documentation: `docs/API.md`
