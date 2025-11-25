"""
Unit tests for FileOrganizer class.
"""

import pytest
import os
import shutil
from pathlib import Path
from src.file_organizer import FileOrganizer
from src.logger import OrganizerLogger


@pytest.fixture
def temp_test_dir(tmp_path):
    """Create a temporary test directory with sample files."""
    test_dir = tmp_path / "test_downloads"
    test_dir.mkdir()

    # Create sample files
    (test_dir / "document.pdf").write_text("PDF content")
    (test_dir / "photo.jpg").write_text("Image content")
    (test_dir / "archive.zip").write_text("Archive content")
    (test_dir / "script.py").write_text("Code content")

    yield test_dir

    # Cleanup
    if test_dir.exists():
        shutil.rmtree(test_dir)


def test_file_organizer_initialization(temp_test_dir):
    """Test FileOrganizer initialization."""
    organizer = FileOrganizer(str(temp_test_dir))
    assert organizer.source_dir == temp_test_dir
    assert organizer.config is not None
    assert organizer.logger is not None


def test_organize_files(temp_test_dir):
    """Test basic file organization."""
    organizer = FileOrganizer(str(temp_test_dir))
    organizer.organize()

    # Check if category folders were created
    assert (temp_test_dir / "Documents").exists()
    assert (temp_test_dir / "Images").exists()
    assert (temp_test_dir / "Archives").exists()
    assert (temp_test_dir / "Code").exists()

    # Check if files were moved
    assert (temp_test_dir / "Documents" / "document.pdf").exists()
    assert (temp_test_dir / "Images" / "photo.jpg").exists()
    assert (temp_test_dir / "Archives" / "archive.zip").exists()
    assert (temp_test_dir / "Code" / "script.py").exists()


def test_organize_dry_run(temp_test_dir):
    """Test dry run mode (no actual file operations)."""
    organizer = FileOrganizer(str(temp_test_dir), dry_run=True)
    organizer.organize()

    # Files should still be in the original location
    assert (temp_test_dir / "document.pdf").exists()
    assert (temp_test_dir / "photo.jpg").exists()
    assert not (temp_test_dir / "Documents").exists()


def test_unique_filename_generation(temp_test_dir):
    """Test handling of duplicate filenames."""
    # Create a file and organize it
    organizer = FileOrganizer(str(temp_test_dir))
    organizer.organize()

    # Create another file with the same name
    (temp_test_dir / "document.pdf").write_text("Another PDF")
    organizer.organize()

    # Check that both files exist with unique names
    docs_dir = temp_test_dir / "Documents"
    pdf_files = list(docs_dir.glob("document*.pdf"))
    assert len(pdf_files) == 2


def test_organize_with_date_folders(temp_test_dir):
    """Test organization with date-based subdirectories."""
    organizer = FileOrganizer(str(temp_test_dir))
    organizer.organize(create_date_folders=True)

    # Check if date folders were created (format: YYYY-MM)
    documents_dir = temp_test_dir / "Documents"
    date_folders = [d for d in documents_dir.iterdir() if d.is_dir()]
    assert len(date_folders) > 0

    # Check date folder name format
    for folder in date_folders:
        assert len(folder.name) == 7  # YYYY-MM format
        assert folder.name[4] == "-"


def test_invalid_source_directory():
    """Test initialization with non-existent directory."""
    with pytest.raises(ValueError):
        FileOrganizer("/nonexistent/directory")
