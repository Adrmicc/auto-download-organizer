"""
Configuration loader for file organization rules.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Loads and manages configuration for file organization."""
    
    DEFAULT_CONFIG = {
        'categories': {
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf', '.tex', '.wpd'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'Programs': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.json', '.xml'],
            'Spreadsheets': ['.xlsx', '.xls', '.csv', '.ods'],
            'Presentations': ['.pptx', '.ppt', '.odp'],
            'Ebooks': ['.epub', '.mobi', '.azw', '.azw3'],
        },
        'settings': {
            'create_date_folders': False,
            'log_file': 'organizer_log.json',
            'dry_run': False,
        }
    }
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration loader.
        
        Args:
            config_path: Path to custom config file. If None, uses default config.
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self.DEFAULT_CONFIG.copy()
    
    def get_category_for_extension(self, extension: str) -> str:
        """
        Get category name for a file extension.
        
        Args:
            extension: File extension (e.g., '.pdf')
            
        Returns:
            Category name or 'Others' if not found
        """
        extension = extension.lower()
        for category, extensions in self.config['categories'].items():
            if extension in extensions:
                return category
        return 'Others'
    
    def get_all_categories(self) -> list:
        """Get list of all category names."""
        return list(self.config['categories'].keys())
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.config.get('settings', {}).get(key, default)
    
    @staticmethod
    def create_default_config(output_path: str):
        """Create a default configuration file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(ConfigLoader.DEFAULT_CONFIG, f, default_flow_style=False)
