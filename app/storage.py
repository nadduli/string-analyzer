from typing import List, Dict, Optional
from datetime import datetime

class Storage:
    def __init__(self):
        self.strings: List[Dict] = []

    def get_all_strings(self) -> List[Dict]:
        return self.strings.copy()
    
    def get_string_by_value(self, value: str) -> Optional[Dict]:
        for string_data in self.strings:
            if string_data["value"] == value:
                return string_data
        return None
    
    def add_string(self, string_data: Dict) -> Dict:
        string_data["id"] = string_data["properties"]["sha256_hash"]
        string_data["created_at"] = datetime.utcnow().isoformat() + "Z"
        
        self.strings.append(string_data)
        return string_data
    
    def delete_string(self, value: str) -> bool:
        for i, string_data in enumerate(self.strings):
            if string_data["value"] == value:
                self.strings.pop(i)
                return True
        return False
    
    def string_exists(self, value: str) -> bool:
        return any(string_data["value"] == value for string_data in self.strings)

storage = Storage()