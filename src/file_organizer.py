"""
File organizer module for managing and categorizing files.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from .config_loader import ConfigLoader
from .logger import OrganizerLogger


class FileOrganizer:
    """Organizes files into categories based on their extensions."""

    def __init__(
        self,
        source_dir: str,
        config_path: str = None,
        logger: OrganizerLogger = None,
        dry_run: bool = False,
    ):
        """
        Initialize file organizer.

        Args:
            source_dir: Source directory to organize (e.g., Downloads folder)
            config_path: Path to configuration file
            logger: Logger instance for tracking operations
            dry_run: If True, only simulate operations without moving files
        """
        self.source_dir = Path(source_dir)
        self.config = ConfigLoader(config_path)
        self.logger = logger or OrganizerLogger()
        self.dry_run = dry_run

        if not self.source_dir.exists():
            raise ValueError(f"Source directory does not exist: {source_dir}")

    def organize(self, create_date_folders: bool = False):
        """
        Organize all files in the source directory.

        Args:
            create_date_folders: If True, create subdirectories based on file date
        """
        print(
            f"\n{'[DRY RUN] ' if self.dry_run else ''}Starting organization of: {self.source_dir}"
        )

        files = [f for f in self.source_dir.iterdir() if f.is_file()]
        print(f"Found {len(files)} files to organize\n")

        for file_path in files:
            try:
                self._organize_file(file_path, create_date_folders)
            except Exception as e:
                self.logger.log_operation(
                    "move", file_path, status="error", details=str(e)
                )
                print(f"Error organizing {file_path.name}: {e}")

        self.logger.save()
        self.logger.print_summary()

    def _organize_file(self, file_path: Path, create_date_folders: bool = False):
        """
        Organize a single file.

        Args:
            file_path: Path to the file
            create_date_folders: Whether to create date-based subdirectories
        """
        # Get category for file
        extension = file_path.suffix.lower()
        category = self.config.get_category_for_extension(extension)

        # Create destination directory
        dest_dir = self.source_dir / category

        if create_date_folders:
            # Get file modification date
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_folder = mod_time.strftime("%Y-%m")
            dest_dir = dest_dir / date_folder

        # Create directory if it doesn't exist
        if not self.dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)

        # Destination file path
        dest_path = dest_dir / file_path.name

        # Handle file name conflicts
        if dest_path.exists():
            dest_path = self._get_unique_filename(dest_path)

        # Move file
        action = f"{'[DRY RUN] ' if self.dry_run else ''}Moving"
        print(f"{action} {file_path.name} -> {category}/{dest_path.name}")

        if not self.dry_run:
            shutil.move(str(file_path), str(dest_path))

        self.logger.log_operation(
            "move",
            file_path,
            dest_path,
            status="success" if not self.dry_run else "dry_run",
            details=f"Organized to {category}",
        )

    def _get_unique_filename(self, file_path: Path) -> Path:
        """
        Generate a unique filename if file already exists.

        Args:
            file_path: Original file path

        Returns:
            Unique file path
        """
        base = file_path.stem
        extension = file_path.suffix
        parent = file_path.parent
        counter = 1

        while True:
            new_name = f"{base}_{counter}{extension}"
            new_path = parent / new_name
            if not new_path.exists():
                return new_path
            counter += 1

    def undo_last_session(self):
        """
        Undo the last organization session.

        Note: This requires the log file to be present.
        """
        if not os.path.exists(self.logger.log_file):
            print("No log file found. Cannot undo.")
            return

        with open(self.logger.log_file, "r", encoding="utf-8") as f:
            logs = json.load(f)

        if not logs:
            print("No operations to undo.")
            return

        last_session = logs[-1]
        operations = last_session.get("operations", [])

        print(f"\nUndoing {len(operations)} operations from last session...")

        for op in reversed(operations):
            if op["type"] == "move" and op["status"] == "success":
                src = Path(op["destination"])
                dst = Path(op["source"])

                if src.exists():
                    shutil.move(str(src), str(dst))
                    print(f"Restored: {src.name} -> {dst}")

        print("\nUndo completed!")
