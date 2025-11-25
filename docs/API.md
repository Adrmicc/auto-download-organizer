# Auto Download Organizer - API Documentation

## Overview

This document provides detailed information about the API and modules of Auto Download Organizer.

## Modules

### file_organizer.py

Main module for organizing files into categories.

#### FileOrganizer Class

```python
class FileOrganizer:
    def __init__(self, source_dir: str, config_path: str = None, 
                 logger: OrganizerLogger = None, dry_run: bool = False)
```

**Parameters:**
- `source_dir`: Directory to organize
- `config_path`: Path to custom configuration file (optional)
- `logger`: Custom logger instance (optional)
- `dry_run`: If True, simulates operations without making changes

**Methods:**

##### organize()
```python
def organize(self, create_date_folders: bool = False)
```
Organizes all files in the source directory.

##### undo_last_session()
```python
def undo_last_session()
```
Reverts the last organization session using log data.

---

### duplicate_cleaner.py

Module for detecting and removing duplicate files.

#### DuplicateCleaner Class

```python
class DuplicateCleaner:
    def __init__(self, directory: str, logger: OrganizerLogger = None, 
                 dry_run: bool = False)
```

**Methods:**

##### find_duplicates()
```python
def find_duplicates(self, recursive: bool = True) -> Dict[str, List[Path]]
```
Returns dictionary mapping file hashes to lists of duplicate files.

##### clean_duplicates()
```python
def clean_duplicates(self, recursive: bool = True, 
                    keep_strategy: str = "newest") -> int
```
Removes duplicate files and returns count of removed files.

**Keep Strategies:**
- `newest`: Keep most recently modified file
- `oldest`: Keep oldest file
- `shortest`: Keep file with shortest name

##### get_duplicate_report()
```python
def get_duplicate_report(self, recursive: bool = True) -> Dict
```
Returns detailed statistics about duplicates without removing them.

---

### logger.py

Comprehensive logging system for tracking operations.

#### OrganizerLogger Class

```python
class OrganizerLogger:
    def __init__(self, log_file: str = "organizer_log.json")
```

**Methods:**

##### log_operation()
```python
def log_operation(self, operation_type: str, source: str, 
                 destination: str = None, status: str = "success", 
                 details: str = None)
```

##### get_summary()
```python
def get_summary() -> Dict[str, Any]
```
Returns statistics summary of all operations.

##### save()
```python
def save()
```
Saves log to JSON file.

---

### config_loader.py

Configuration management system.

#### ConfigLoader Class

```python
class ConfigLoader:
    def __init__(self, config_path: str = None)
```

**Methods:**

##### get_category_for_extension()
```python
def get_category_for_extension(self, extension: str) -> str
```
Returns category name for a file extension.

##### get_all_categories()
```python
def get_all_categories() -> list
```
Returns list of all category names.

##### get_setting()
```python
def get_setting(self, key: str, default: Any = None) -> Any
```
Retrieves a configuration setting value.

---

## CLI Commands

### organize
```powershell
python -m src.cli organize [OPTIONS]
```

**Options:**
- `--directory, -d`: Directory to organize
- `--config, -c`: Custom config file path
- `--date-folders`: Create date-based subdirectories
- `--dry-run`: Simulate without making changes
- `--log-file`: Custom log file path

### clean-duplicates
```powershell
python -m src.cli clean-duplicates [OPTIONS]
```

**Options:**
- `--directory, -d`: Directory to scan
- `--recursive, -r`: Scan subdirectories
- `--keep`: Keep strategy (newest/oldest/shortest)
- `--dry-run`: Simulate without deleting
- `--report-only`: Show report only

### full
```powershell
python -m src.cli full [OPTIONS]
```

**Options:**
- `--directory, -d`: Directory to process (required)
- `--config, -c`: Custom config file
- `--date-folders`: Create date folders
- `--clean-duplicates`: Also remove duplicates
- `--keep`: Keep strategy for duplicates
- `--dry-run`: Simulate operations

### create-config
```powershell
python -m src.cli create-config OUTPUT_PATH
```

### show-log
```powershell
python -m src.cli show-log [--log-file PATH]
```

---

## Configuration File Format

```yaml
categories:
  CategoryName:
    - .ext1
    - .ext2

settings:
  create_date_folders: false
  log_file: organizer_log.json
  dry_run: false
```

---

## Log File Format

```json
[
  {
    "session_start": "2025-11-25T10:00:00",
    "session_end": "2025-11-25T10:05:00",
    "total_operations": 50,
    "by_type": {
      "move": 45,
      "delete_duplicate": 5
    },
    "by_status": {
      "success": 49,
      "error": 1
    },
    "operations": [
      {
        "timestamp": "2025-11-25T10:00:01",
        "type": "move",
        "source": "/downloads/file.pdf",
        "destination": "/downloads/Documents/file.pdf",
        "status": "success",
        "details": "Organized to Documents"
      }
    ]
  }
]
```

---

## Error Handling

All modules implement comprehensive error handling:

- Invalid directories raise `ValueError`
- File operation errors are logged with details
- Dry run mode prevents accidental changes
- All errors are captured in logs

---

## Examples

### Programmatic Usage

```python
from src.file_organizer import FileOrganizer
from src.duplicate_cleaner import DuplicateCleaner
from src.logger import OrganizerLogger

# Setup logger
logger = OrganizerLogger("my_log.json")

# Organize files
organizer = FileOrganizer("C:/Downloads", logger=logger)
organizer.organize(create_date_folders=True)

# Clean duplicates
cleaner = DuplicateCleaner("C:/Downloads", logger=logger)
removed = cleaner.clean_duplicates(keep_strategy="newest")

# Save log
logger.save()
logger.print_summary()
```
