#!/usr/bin/python3
"""This module defines a Storage class for managing data storage."""

from typing import List, Dict, Optional
from datetime import datetime
import uuid

class Storage:

    def __init__(self):
        """Initialize variables"""
        self.strings: List[Dict] = []

    def get_all_strings(self) -> List[Dict]:
        """return all strings"""
        return self.strings.copy()
    
    def get_string_by_value(self, value: str) -> Optional[Dict]:
        """Returns a string by its value"""
        for string_data in self.strings:
            if string_data["value"] == value:
                return string_data
        return None
    
    def get_string_by_id(self, string_id: str) -> Optional[Dict]:
        """return a string by its id"""
        for string_data in self.strings:
            if string_data["id"] == string_id:
                return string_data
        return None
    
    def add_string(self, string_data: Dict) -> Dict:
        """Add a new string to the storage"""
        string_data["id"] = string_data["properties"]["sha256_hash"][:8]
        string_data["created_at"] = datetime.utcnow().isoformat()

        self.strings.append(string_data)
        return string_data
    
    def delete_string(self, value: str) -> bool:
        """Delete string by value"""

        for i, string_data in enumerate(self.strings):
            if string_data["value"] == value:
                self.strings.pop(i)
                return True
            
        return False
    
    def string_exists(self, value:str) -> bool:
        """Check if a string already exists"""
        return any(string_data["value"] == value for string_data in self.strings)
    

storage = Storage()
