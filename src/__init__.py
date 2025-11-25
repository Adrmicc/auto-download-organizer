"""
Auto Download Organizer
A professional tool for automatically organizing your Downloads folder.
"""

__version__ = "1.0.0"
__author__ = "Adrmicc"

from .file_organizer import FileOrganizer
from .duplicate_cleaner import DuplicateCleaner
from .logger import OrganizerLogger

__all__ = ["FileOrganizer", "DuplicateCleaner", "OrganizerLogger"]
