# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please let me know.

## Security Best Practices for Users

When using Auto Download Organizer:

1. **Backup Your Files**: Always backup important files before running the organizer
2. **Test with Dry Run**: Use `--dry-run` flag to preview operations
3. **Review Logs**: Check operation logs regularly
4. **Custom Configurations**: Validate custom config files before use
5. **Permissions**: Run with appropriate user permissions (avoid running as admin unless necessary)
6. **Virtual Environment**: Use a virtual environment to isolate dependencies
7. **Update Regularly**: Keep the tool and its dependencies up to date

## Known Security Considerations

### File Operations
- The tool moves and deletes files - always backup important data
- Dry run mode is recommended for first-time use
- Log files contain full file paths - keep them secure

### Dependencies
- Keep dependencies updated (`pip install --upgrade -r requirements.txt`)
- Review dependency security advisories
- Use virtual environments to prevent conflicts

### Configuration Files
- YAML files are parsed - validate custom configs
- Avoid running configs from untrusted sources
- Keep config files in secure locations

## Updates and Patches

Security updates will be:
- Released as soon as possible after verification
- Announced in CHANGELOG.md
- Tagged with version numbers following semantic versioning

## Contact

For general issues: Open a GitHub issue
