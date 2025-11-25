"""
Unit tests for ConfigLoader class.
"""

import pytest
import yaml
from pathlib import Path
from src.config_loader import ConfigLoader


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file."""
    config_file = tmp_path / "test_config.yaml"

    config_data = {
        "categories": {"TestDocs": [".test", ".doc"], "TestImages": [".img", ".pic"]},
        "settings": {"test_setting": True},
    }

    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)

    yield str(config_file)


def test_default_config():
    """Test loading default configuration."""
    config = ConfigLoader()

    # Check default categories
    assert "Documents" in config.config["categories"]
    assert "Images" in config.config["categories"]
    assert "Videos" in config.config["categories"]

    # Check default settings
    assert "settings" in config.config


def test_load_custom_config(temp_config_file):
    """Test loading custom configuration."""
    config = ConfigLoader(temp_config_file)

    assert "TestDocs" in config.config["categories"]
    assert "TestImages" in config.config["categories"]
    assert config.config["settings"]["test_setting"] is True


def test_get_category_for_extension():
    """Test getting category for file extension."""
    config = ConfigLoader()

    assert config.get_category_for_extension(".pdf") == "Documents"
    assert config.get_category_for_extension(".jpg") == "Images"
    assert config.get_category_for_extension(".mp4") == "Videos"
    assert config.get_category_for_extension(".xyz") == "Others"


def test_get_category_case_insensitive():
    """Test that extension matching is case-insensitive."""
    config = ConfigLoader()

    assert config.get_category_for_extension(".PDF") == "Documents"
    assert config.get_category_for_extension(".JPG") == "Images"


def test_get_all_categories():
    """Test getting all category names."""
    config = ConfigLoader()
    categories = config.get_all_categories()

    assert "Documents" in categories
    assert "Images" in categories
    assert isinstance(categories, list)


def test_get_setting():
    """Test getting setting values."""
    config = ConfigLoader()

    log_file = config.get_setting("log_file")
    assert log_file == "organizer_log.json"

    # Test with default value
    unknown = config.get_setting("unknown_setting", "default_value")
    assert unknown == "default_value"


def test_create_default_config(tmp_path):
    """Test creating a default config file."""
    output_file = tmp_path / "new_config.yaml"
    ConfigLoader.create_default_config(str(output_file))

    assert output_file.exists()

    # Verify content
    with open(output_file, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)

    assert "categories" in config_data
    assert "settings" in config_data
