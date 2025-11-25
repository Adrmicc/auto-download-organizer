"""
Unit tests for DuplicateCleaner class.
"""

import pytest
import shutil
from pathlib import Path
from src.duplicate_cleaner import DuplicateCleaner


@pytest.fixture
def temp_test_dir(tmp_path):
    """Create a temporary test directory with duplicate files."""
    test_dir = tmp_path / "test_duplicates"
    test_dir.mkdir()
    
    # Create duplicate files (same content)
    content = "This is duplicate content"
    (test_dir / "file1.txt").write_text(content)
    (test_dir / "file2.txt").write_text(content)
    (test_dir / "file3.txt").write_text(content)
    
    # Create a unique file
    (test_dir / "unique.txt").write_text("This is unique content")
    
    yield test_dir
    
    # Cleanup
    if test_dir.exists():
        shutil.rmtree(test_dir)


def test_duplicate_cleaner_initialization(temp_test_dir):
    """Test DuplicateCleaner initialization."""
    cleaner = DuplicateCleaner(str(temp_test_dir))
    assert cleaner.directory == temp_test_dir
    assert cleaner.logger is not None


def test_find_duplicates(temp_test_dir):
    """Test finding duplicate files."""
    cleaner = DuplicateCleaner(str(temp_test_dir))
    duplicates = cleaner.find_duplicates(recursive=False)
    
    # Should find one set of duplicates (3 files with same content)
    assert len(duplicates) == 1
    
    # Get the duplicate set
    duplicate_set = list(duplicates.values())[0]
    assert len(duplicate_set) == 3


def test_clean_duplicates(temp_test_dir):
    """Test removing duplicate files."""
    cleaner = DuplicateCleaner(str(temp_test_dir))
    removed = cleaner.clean_duplicates(recursive=False, keep_strategy="newest")
    
    # Should remove 2 duplicates (keeping 1)
    assert removed == 2
    
    # Should have 2 files remaining (1 from duplicate set + 1 unique)
    remaining_files = list(temp_test_dir.glob("*.txt"))
    assert len(remaining_files) == 2


def test_clean_duplicates_dry_run(temp_test_dir):
    """Test dry run mode for duplicate cleaning."""
    cleaner = DuplicateCleaner(str(temp_test_dir), dry_run=True)
    cleaner.clean_duplicates(recursive=False)
    
    # All files should still exist
    files = list(temp_test_dir.glob("*.txt"))
    assert len(files) == 4


def test_duplicate_report(temp_test_dir):
    """Test generating duplicate report."""
    cleaner = DuplicateCleaner(str(temp_test_dir))
    report = cleaner.get_duplicate_report(recursive=False)
    
    assert report["duplicate_sets"] == 1
    assert report["total_files_involved"] == 3
    assert report["total_duplicates"] == 2
    assert report["wasted_space_bytes"] > 0


def test_keep_strategy_newest(temp_test_dir):
    """Test keeping the newest duplicate."""
    import time
    
    # Make file3 the newest by touching it
    file3 = temp_test_dir / "file3.txt"
    time.sleep(0.1)
    file3.touch()
    
    cleaner = DuplicateCleaner(str(temp_test_dir))
    cleaner.clean_duplicates(recursive=False, keep_strategy="newest")
    
    # file3 should still exist
    assert file3.exists()


def test_keep_strategy_shortest(temp_test_dir):
    """Test keeping the file with shortest name."""
    # Rename files to have different lengths
    (temp_test_dir / "file1.txt").rename(temp_test_dir / "a.txt")
    (temp_test_dir / "file2.txt").rename(temp_test_dir / "longer_name.txt")
    
    cleaner = DuplicateCleaner(str(temp_test_dir))
    cleaner.clean_duplicates(recursive=False, keep_strategy="shortest")
    
    # "a.txt" should still exist (shortest name)
    assert (temp_test_dir / "a.txt").exists()


def test_invalid_directory():
    """Test initialization with non-existent directory."""
    with pytest.raises(ValueError):
        DuplicateCleaner("/nonexistent/directory")
