# app/utils/analyzer.py
import hashlib
from typing import Dict

class StringAnalyzer:
    @staticmethod
    def analyze_string(value: str) -> Dict:
        """Analyze string and return all properties"""
        trimmed_value = value.strip()
        
        return {
            "length": StringAnalyzer.get_string_length(trimmed_value),
            "is_palindrome": StringAnalyzer.is_palindrome(trimmed_value),
            "unique_characters": StringAnalyzer.get_unique_characters_count(trimmed_value),
            "word_count": StringAnalyzer.get_word_count(trimmed_value),
            "sha256_hash": StringAnalyzer.generate_sha256_hash(trimmed_value),
            "character_frequency_map": StringAnalyzer.get_character_frequency(trimmed_value)
        }

    @staticmethod
    def get_string_length(string: str) -> int:
        return len(string)

    @staticmethod
    def is_palindrome(string: str) -> bool:
        if not string:
            return True
            
        clean_string = ''.join(char.lower() for char in string if char.isalnum())
        return clean_string == clean_string[::-1]

    @staticmethod
    def get_unique_characters_count(string: str) -> int:
        return len(set(string.lower()))

    @staticmethod
    def get_word_count(string: str) -> int:
        words = string.split()
        return len(words) if string.strip() else 0

    @staticmethod
    def generate_sha256_hash(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    @staticmethod
    def get_character_frequency(string: str) -> Dict[str, int]:
        frequency = {}
        for char in string.lower():
            frequency[char] = frequency.get(char, 0) + 1
        return frequency