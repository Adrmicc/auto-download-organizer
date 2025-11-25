# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-25

### Added
- Initial release of Auto Download Organizer
- File organization by category (Documents, Images, Videos, etc.)
- Duplicate file detection using SHA256 hashing
- Comprehensive JSON logging system
- CLI interface with multiple commands
- Dry run mode for safe testing
- Date-based folder organization option
- Multiple duplicate keep strategies (newest, oldest, shortest)
- YAML-based configuration system
- Full test suite with pytest
- Complete documentation (README, API docs, examples)
- MIT License

### Features
- **organize** command - Organize files into categories
- **clean-duplicates** command - Find and remove duplicate files
- **full** command - Complete organization workflow
- **create-config** command - Generate custom configuration
- **show-log** command - View operation history
- Custom configuration support
- Recursive directory scanning
- Detailed operation logging
- Error handling and recovery

### Documentation
- Comprehensive README with badges
- API documentation
- Quick start guide
- Contributing guidelines
- Polish language instructions (INSTRUKCJA_PL.md)
- Usage examples

### Testing
- Unit tests for all core modules
- Test coverage for file organizer
- Test coverage for duplicate cleaner
- Test coverage for logger
- Test coverage for config loader

## [Unreleased]

### Planned Features
- GUI interface (Tkinter/PyQt)
- Scheduled automatic organization
- Watch mode for real-time organization
- Cloud storage integration (Google Drive, Dropbox)
- Email notifications for organization reports
- Undo functionality for accidental operations
- File preview before organization
- Statistics dashboard
- Multiple language support
- Docker container support
