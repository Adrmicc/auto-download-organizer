"""
Unit tests for OrganizerLogger class.
"""

import pytest
import json
import os
from pathlib import Path
from src.logger import OrganizerLogger


@pytest.fixture
def temp_log_file(tmp_path):
    """Create a temporary log file path."""
    log_file = tmp_path / "test_log.json"
    yield str(log_file)
    
    # Cleanup
    if os.path.exists(log_file):
        os.remove(log_file)


def test_logger_initialization(temp_log_file):
    """Test OrganizerLogger initialization."""
    logger = OrganizerLogger(temp_log_file)
    assert logger.log_file == temp_log_file
    assert logger.operations == []
    assert logger.session_start is not None


def test_log_operation(temp_log_file):
    """Test logging an operation."""
    logger = OrganizerLogger(temp_log_file)
    logger.log_operation(
        "move",
        "/source/file.txt",
        "/destination/file.txt",
        status="success",
        details="Test operation"
    )
    
    assert len(logger.operations) == 1
    op = logger.operations[0]
    assert op["type"] == "move"
    assert op["source"] == "/source/file.txt"
    assert op["destination"] == "/destination/file.txt"
    assert op["status"] == "success"


def test_get_summary(temp_log_file):
    """Test getting operation summary."""
    logger = OrganizerLogger(temp_log_file)
    
    # Log multiple operations
    logger.log_operation("move", "/file1.txt", "/dest/file1.txt", status="success")
    logger.log_operation("move", "/file2.txt", "/dest/file2.txt", status="success")
    logger.log_operation("delete_duplicate", "/file3.txt", status="success")
    logger.log_operation("move", "/file4.txt", status="error")
    
    summary = logger.get_summary()
    
    assert summary["total_operations"] == 4
    assert summary["by_type"]["move"] == 3
    assert summary["by_type"]["delete_duplicate"] == 1
    assert summary["by_status"]["success"] == 3
    assert summary["by_status"]["error"] == 1


def test_save_log(temp_log_file):
    """Test saving log to file."""
    logger = OrganizerLogger(temp_log_file)
    logger.log_operation("move", "/file.txt", "/dest/file.txt", status="success")
    logger.save()
    
    assert os.path.exists(temp_log_file)
    
    # Verify log content
    with open(temp_log_file, 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    assert isinstance(logs, list)
    assert len(logs) == 1
    assert logs[0]["total_operations"] == 1


def test_append_to_existing_log(temp_log_file):
    """Test appending to an existing log file."""
    # First session
    logger1 = OrganizerLogger(temp_log_file)
    logger1.log_operation("move", "/file1.txt", "/dest/file1.txt", status="success")
    logger1.save()
    
    # Second session
    logger2 = OrganizerLogger(temp_log_file)
    logger2.log_operation("move", "/file2.txt", "/dest/file2.txt", status="success")
    logger2.save()
    
    # Verify both sessions are in the log
    with open(temp_log_file, 'r', encoding='utf-8') as f:
        logs = json.load(f)
    
    assert len(logs) == 2


def test_empty_log(temp_log_file):
    """Test behavior with no operations logged."""
    logger = OrganizerLogger(temp_log_file)
    summary = logger.get_summary()
    
    assert summary["total_operations"] == 0
    assert summary["by_type"] == {}
    assert summary["by_status"] == {}
