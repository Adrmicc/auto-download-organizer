"""
Duplicate file cleaner module.
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

from .logger import OrganizerLogger


class DuplicateCleaner:
    """Finds and removes duplicate files based on content hash."""
    
    def __init__(self, directory: str, logger: OrganizerLogger = None, 
                 dry_run: bool = False):
        """
        Initialize duplicate cleaner.
        
        Args:
            directory: Directory to scan for duplicates
            logger: Logger instance for tracking operations
            dry_run: If True, only simulate operations without deleting files
        """
        self.directory = Path(directory)
        self.logger = logger or OrganizerLogger()
        self.dry_run = dry_run
        
        if not self.directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
    
    def find_duplicates(self, recursive: bool = True) -> Dict[str, List[Path]]:
        """
        Find duplicate files in the directory.
        
        Args:
            recursive: If True, scan subdirectories recursively
            
        Returns:
            Dictionary mapping file hashes to lists of file paths
        """
        print(f"\n{'[DRY RUN] ' if self.dry_run else ''}Scanning for duplicates in: {self.directory}")
        
        hash_map = defaultdict(list)
        
        # Get all files
        if recursive:
            files = [f for f in self.directory.rglob('*') if f.is_file()]
        else:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        
        print(f"Scanning {len(files)} files...")
        
        # Calculate hashes
        for file_path in files:
            try:
                file_hash = self._calculate_hash(file_path)
                hash_map[file_hash].append(file_path)
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
        
        # Filter to only duplicates (hash appears more than once)
        duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
        
        return duplicates
    
    def clean_duplicates(self, recursive: bool = True, 
                        keep_strategy: str = "newest") -> int:
        """
        Find and remove duplicate files.
        
        Args:
            recursive: If True, scan subdirectories recursively
            keep_strategy: Strategy for which file to keep:
                          - "newest": Keep the newest file (by modification time)
                          - "oldest": Keep the oldest file
                          - "shortest": Keep file with shortest name
                          
        Returns:
            Number of files removed
        """
        duplicates = self.find_duplicates(recursive)
        
        if not duplicates:
            print("\nNo duplicates found!")
            return 0
        
        total_duplicates = sum(len(paths) - 1 for paths in duplicates.values())
        print(f"\nFound {len(duplicates)} sets of duplicates ({total_duplicates} files to remove)")
        
        removed_count = 0
        
        for file_hash, paths in duplicates.items():
            # Determine which file to keep
            if keep_strategy == "newest":
                keep_file = max(paths, key=lambda p: p.stat().st_mtime)
            elif keep_strategy == "oldest":
                keep_file = min(paths, key=lambda p: p.stat().st_mtime)
            elif keep_strategy == "shortest":
                keep_file = min(paths, key=lambda p: len(p.name))
            else:
                keep_file = paths[0]
            
            print(f"\nDuplicate set (hash: {file_hash[:8]}...):")
            print(f"  Keeping: {keep_file}")
            
            # Remove duplicates
            for path in paths:
                if path != keep_file:
                    print(f"  {'[DRY RUN] ' if self.dry_run else ''}Removing: {path}")
                    
                    if not self.dry_run:
                        path.unlink()
                    
                    self.logger.log_operation(
                        "delete_duplicate",
                        path,
                        destination=str(keep_file),
                        status="success" if not self.dry_run else "dry_run",
                        details=f"Duplicate of {keep_file.name}"
                    )
                    removed_count += 1
        
        self.logger.save()
        print(f"\n{'[DRY RUN] ' if self.dry_run else ''}Removed {removed_count} duplicate files")
        
        return removed_count
    
    def _calculate_hash(self, file_path: Path, block_size: int = 65536) -> str:
        """
        Calculate SHA256 hash of a file.
        
        Args:
            file_path: Path to the file
            block_size: Size of blocks to read at a time
            
        Returns:
            Hexadecimal hash string
        """
        hasher = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            while True:
                block = f.read(block_size)
                if not block:
                    break
                hasher.update(block)
        
        return hasher.hexdigest()
    
    def get_duplicate_report(self, recursive: bool = True) -> Dict:
        """
        Get a detailed report of duplicates without removing them.
        
        Args:
            recursive: If True, scan subdirectories recursively
            
        Returns:
            Dictionary with duplicate statistics and details
        """
        duplicates = self.find_duplicates(recursive)
        
        total_files = sum(len(paths) for paths in duplicates.values())
        total_duplicates = sum(len(paths) - 1 for paths in duplicates.values())
        
        # Calculate wasted space
        wasted_space = 0
        for paths in duplicates.values():
            file_size = paths[0].stat().st_size
            wasted_space += file_size * (len(paths) - 1)
        
        report = {
            "duplicate_sets": len(duplicates),
            "total_files_involved": total_files,
            "total_duplicates": total_duplicates,
            "wasted_space_bytes": wasted_space,
            "wasted_space_mb": round(wasted_space / (1024 * 1024), 2),
            "details": []
        }
        
        for file_hash, paths in duplicates.items():
            file_size = paths[0].stat().st_size
            report["details"].append({
                "hash": file_hash[:16],
                "count": len(paths),
                "size_bytes": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "files": [str(p) for p in paths]
            })
        
        return report
