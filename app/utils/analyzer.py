import hashlib
import re
from typing import Dict

class StringAnalyzer:
    @staticmethod
    def analyze_string(value: str) -> Dict:
        """Analyze string and return all properties"""
        if value is None:
            raise ValueError("String value cannot be None")
            
        return {
            "length": StringAnalyzer.get_string_length(value),
            "is_palindrome": StringAnalyzer.is_palindrome(value),
            "unique_characters": StringAnalyzer.get_unique_characters_count(value),
            "word_count": StringAnalyzer.get_word_count(value),
            "sha256_hash": StringAnalyzer.generate_sha256_hash(value),
            "character_frequency_map": StringAnalyzer.get_character_frequency(value)
        }

    @staticmethod
    def get_string_length(string: str) -> int:
        return len(string)

    @staticmethod
    def is_palindrome(string: str) -> bool:
        """Case-insensitive palindrome check (only alphanumeric characters)"""
        if not string:
            return True
            
        clean_string = re.sub(r'[^a-zA-Z0-9]', '', string).lower()
        if not clean_string:
            return True
            
        return clean_string == clean_string[::-1]

    @staticmethod
    def get_unique_characters_count(string: str) -> int:
        return len(set(string.lower()))

    @staticmethod
    def get_word_count(string: str) -> int:
        if not string.strip():
            return 0
        return len(string.split())

    @staticmethod
    def generate_sha256_hash(string: str) -> str:
        """Generate SHA256 hash as hex string"""
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    @staticmethod
    def get_character_frequency(string: str) -> Dict[str, int]:
        frequency = {}
        for char in string.lower():
            frequency[char] = frequency.get(char, 0) + 1
        return frequency