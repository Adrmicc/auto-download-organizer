"""
Command-line interface for Auto Download Organizer.
"""

import click
import os
from pathlib import Path

from .file_organizer import FileOrganizer
from .duplicate_cleaner import DuplicateCleaner
from .logger import OrganizerLogger
from .config_loader import ConfigLoader


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Auto Download Organizer - Automatically organize your Downloads folder.
    
    A professional tool to keep your files organized with automatic categorization,
    duplicate detection, and detailed logging.
    """
    pass


@cli.command()
@click.option(
    '--directory', '-d',
    type=click.Path(exists=True),
    default=None,
    help='Directory to organize (default: Downloads folder)'
)
@click.option(
    '--config', '-c',
    type=click.Path(exists=True),
    default=None,
    help='Path to custom configuration file'
)
@click.option(
    '--date-folders',
    is_flag=True,
    help='Create subdirectories based on file modification date (YYYY-MM)'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Simulate operations without actually moving files'
)
@click.option(
    '--log-file',
    type=str,
    default='organizer_log.json',
    help='Path to log file (default: organizer_log.json)'
)
def organize(directory, config, date_folders, dry_run, log_file):
    """Organize files in the specified directory."""
    
    # Use Downloads folder if no directory specified
    if not directory:
        directory = str(Path.home() / 'Downloads')
        click.echo(f"No directory specified, using: {directory}")
    
    if not os.path.exists(directory):
        click.echo(f"Error: Directory does not exist: {directory}", err=True)
        return
    
    try:
        logger = OrganizerLogger(log_file)
        organizer = FileOrganizer(directory, config, logger, dry_run)
        organizer.organize(create_date_folders=date_folders)
        
        if dry_run:
            click.echo("\nThis was a dry run. No files were actually moved.")
        else:
            click.echo(f"\nOrganization complete! Log saved to: {log_file}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.option(
    '--directory', '-d',
    type=click.Path(exists=True),
    default=None,
    help='Directory to scan for duplicates (default: Downloads folder)'
)
@click.option(
    '--recursive', '-r',
    is_flag=True,
    default=True,
    help='Scan subdirectories recursively (default: True)'
)
@click.option(
    '--keep',
    type=click.Choice(['newest', 'oldest', 'shortest']),
    default='newest',
    help='Strategy for which duplicate to keep (default: newest)'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Simulate operations without actually deleting files'
)
@click.option(
    '--report-only',
    is_flag=True,
    help='Only show duplicate report without removing files'
)
@click.option(
    '--log-file',
    type=str,
    default='organizer_log.json',
    help='Path to log file (default: organizer_log.json)'
)
def clean_duplicates(directory, recursive, keep, dry_run, report_only, log_file):
    """Find and remove duplicate files."""
    
    # Use Downloads folder if no directory specified
    if not directory:
        directory = str(Path.home() / 'Downloads')
        click.echo(f"No directory specified, using: {directory}")
    
    if not os.path.exists(directory):
        click.echo(f"Error: Directory does not exist: {directory}", err=True)
        return
    
    try:
        logger = OrganizerLogger(log_file)
        cleaner = DuplicateCleaner(directory, logger, dry_run)
        
        if report_only:
            report = cleaner.get_duplicate_report(recursive)
            click.echo("\n" + "="*50)
            click.echo("DUPLICATE FILES REPORT")
            click.echo("="*50)
            click.echo(f"Duplicate sets: {report['duplicate_sets']}")
            click.echo(f"Total files involved: {report['total_files_involved']}")
            click.echo(f"Total duplicates: {report['total_duplicates']}")
            click.echo(f"Wasted space: {report['wasted_space_mb']} MB")
            click.echo("="*50)
        else:
            cleaner.clean_duplicates(recursive, keep)
            
            if dry_run:
                click.echo("\nThis was a dry run. No files were actually deleted.")
            else:
                click.echo(f"\nCleaning complete! Log saved to: {log_file}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument('output_path', type=click.Path())
def create_config(output_path):
    """Create a default configuration file."""
    
    try:
        ConfigLoader.create_default_config(output_path)
        click.echo(f"Configuration file created: {output_path}")
        click.echo("You can now customize it and use with --config option")
    
    except Exception as e:
        click.echo(f"Error creating config: {e}", err=True)


@cli.command()
@click.option(
    '--log-file',
    type=click.Path(exists=True),
    default='organizer_log.json',
    help='Path to log file (default: organizer_log.json)'
)
def show_log(log_file):
    """Display the organization log."""
    
    if not os.path.exists(log_file):
        click.echo(f"Log file not found: {log_file}", err=True)
        return
    
    try:
        import json
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        if not logs:
            click.echo("No logs found.")
            return
        
        for i, session in enumerate(logs, 1):
            click.echo(f"\n{'='*50}")
            click.echo(f"Session {i}")
            click.echo(f"{'='*50}")
            click.echo(f"Start: {session['session_start']}")
            click.echo(f"End: {session['session_end']}")
            click.echo(f"Total operations: {session['total_operations']}")
            
            if session.get('by_type'):
                click.echo("\nOperations by type:")
                for op_type, count in session['by_type'].items():
                    click.echo(f"  {op_type}: {count}")
    
    except Exception as e:
        click.echo(f"Error reading log: {e}", err=True)


@cli.command()
@click.option(
    '--directory', '-d',
    type=click.Path(exists=True),
    required=True,
    help='Directory to organize and clean'
)
@click.option(
    '--config', '-c',
    type=click.Path(exists=True),
    default=None,
    help='Path to custom configuration file'
)
@click.option(
    '--date-folders',
    is_flag=True,
    help='Create subdirectories based on file modification date'
)
@click.option(
    '--clean-duplicates',
    is_flag=True,
    help='Also remove duplicate files'
)
@click.option(
    '--keep',
    type=click.Choice(['newest', 'oldest', 'shortest']),
    default='newest',
    help='Strategy for which duplicate to keep (default: newest)'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Simulate operations without making changes'
)
def full(directory, config, date_folders, clean_duplicates, keep, dry_run):
    """Run full organization process (organize + clean duplicates)."""
    
    click.echo("Starting full organization process...")
    
    try:
        logger = OrganizerLogger()
        
        # Step 1: Organize files
        click.echo("\n[Step 1/2] Organizing files...")
        organizer = FileOrganizer(directory, config, logger, dry_run)
        organizer.organize(create_date_folders=date_folders)
        
        # Step 2: Clean duplicates
        if clean_duplicates:
            click.echo("\n[Step 2/2] Cleaning duplicates...")
            cleaner = DuplicateCleaner(directory, logger, dry_run)
            cleaner.clean_duplicates(recursive=True, keep_strategy=keep)
        else:
            click.echo("\n[Step 2/2] Skipping duplicate cleaning (use --clean-duplicates to enable)")
        
        logger.save()
        
        if dry_run:
            click.echo("\nThis was a dry run. No actual changes were made.")
        else:
            click.echo("\nFull organization complete!")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
