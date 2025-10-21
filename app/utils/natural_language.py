import re
from typing import Dict, Any

class NaturalLanguageParser:
    @staticmethod
    def parse_query(query: str) -> Dict[str, Any]:
        """Parse natural language query into filters"""
        filters = {}
        lower_query = query.lower().strip()

        if any(word in lower_query for word in ['palindrome', 'palindromic']):
            filters['is_palindrome'] = True

        word_count_patterns = [
            (r'single word|one word', 1),
            (r'two words', 2),
            (r'three words', 3),
            (r'four words', 4),
            (r'five words', 5),
            (r'(\d+) words?', None)
        ]

        for pattern, count in word_count_patterns:
            match = re.search(pattern, lower_query)
            if match:
                if count is not None:
                    filters['word_count'] = count
                else:
                    filters['word_count'] = int(match.group(1))
                break

        longer_match = re.search(r'(longer|greater|more than|over)\s+(\d+)', lower_query)
        if longer_match:
            filters['min_length'] = int(longer_match.group(2)) + 1

        shorter_match = re.search(r'(shorter|less than|under)\s+(\d+)', lower_query)
        if shorter_match:
            filters['max_length'] = int(shorter_match.group(2)) - 1

        exact_length_match = re.search(r'exactly\s+(\d+)\s+characters', lower_query)
        if exact_length_match:
            length = int(exact_length_match.group(1))
            filters['min_length'] = length
            filters['max_length'] = length

        char_match = re.search(r'contain(s|ing)?\s+(?:the\s+)?(?:letter\s+)?([a-z])', lower_query)
        if char_match:
            filters['contains_character'] = char_match.group(2)

        for char in 'abcdefghijklmnopqrstuvwxyz':
            if f'contains {char}' in lower_query or f'has {char}' in lower_query:
                filters['contains_character'] = char
                break

        if 'vowel' in lower_query:
            filters['contains_character'] = 'a'

        return filters

    @staticmethod
    def validate_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean filters"""
        validated = {}
        
        for key, value in filters.items():
            if value is not None:
                validated[key] = value

        if 'min_length' in validated and 'max_length' in validated:
            if validated['min_length'] > validated['max_length']:
                raise ValueError("Conflicting filters: min_length cannot be greater than max_length")

        return validated