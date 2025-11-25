"""
Logger module for tracking file operations.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class OrganizerLogger:
    """Logs all file operations to a JSON file."""
    
    def __init__(self, log_file: str = "organizer_log.json"):
        """
        Initialize logger.
        
        Args:
            log_file: Path to the log file
        """
        self.log_file = log_file
        self.operations = []
        self.session_start = datetime.now().isoformat()
    
    def log_operation(self, operation_type: str, source: str, 
                     destination: str = None, status: str = "success", 
                     details: str = None):
        """
        Log a file operation.
        
        Args:
            operation_type: Type of operation (move, delete, skip, etc.)
            source: Source file path
            destination: Destination path (if applicable)
            status: Operation status (success, error, skipped)
            details: Additional details or error message
        """
        operation = {
            "timestamp": datetime.now().isoformat(),
            "type": operation_type,
            "source": str(source),
            "destination": str(destination) if destination else None,
            "status": status,
            "details": details
        }
        self.operations.append(operation)
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of all operations.
        
        Returns:
            Dictionary with operation statistics
        """
        summary = {
            "session_start": self.session_start,
            "session_end": datetime.now().isoformat(),
            "total_operations": len(self.operations),
            "by_type": {},
            "by_status": {},
            "operations": self.operations
        }
        
        for op in self.operations:
            op_type = op["type"]
            status = op["status"]
            
            summary["by_type"][op_type] = summary["by_type"].get(op_type, 0) + 1
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        
        return summary
    
    def save(self):
        """Save log to file."""
        summary = self.get_summary()
        
        # Load existing logs if file exists
        existing_logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    existing_logs = json.load(f)
                    if not isinstance(existing_logs, list):
                        existing_logs = [existing_logs]
            except json.JSONDecodeError:
                existing_logs = []
        
        # Append new session
        existing_logs.append(summary)
        
        # Save to file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(existing_logs, f, indent=2, ensure_ascii=False)
    
    def print_summary(self):
        """Print a human-readable summary to console."""
        summary = self.get_summary()
        
        print("\n" + "="*50)
        print("ORGANIZATION SUMMARY")
        print("="*50)
        print(f"Session: {summary['session_start']} - {summary['session_end']}")
        print(f"Total operations: {summary['total_operations']}")
        
        if summary['by_type']:
            print("\nOperations by type:")
            for op_type, count in summary['by_type'].items():
                print(f"  {op_type}: {count}")
        
        if summary['by_status']:
            print("\nOperations by status:")
            for status, count in summary['by_status'].items():
                print(f"  {status}: {count}")
        
        print("="*50 + "\n")
