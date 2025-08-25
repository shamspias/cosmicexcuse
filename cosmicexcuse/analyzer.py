"""
Error severity analyzer module.
"""

import re
from typing import Dict, List


class SeverityAnalyzer:
    """
    Analyzes error messages to determine severity level.
    """

    def __init__(self):
        """Initialize the severity analyzer."""
        self.severity_keywords = {
            'severe': [
                'fatal', 'critical', 'crash', 'panic', 'doom', 'catastrophic',
                'emergency', 'disaster', 'meltdown', 'apocalypse', 'dead',
                'explosion', 'fire', 'burning', 'destroyed', 'corrupted'
            ],
            'medium': [
                'error', 'fail', 'failed', 'exception', 'warning', 'problem',
                'issue', 'broken', 'invalid', 'denied', 'refused', 'timeout',
                'overflow', 'leak', 'violation', 'conflict'
            ],
            'mild': [
                'notice', 'info', 'debug', 'trace', 'minor', 'slight',
                'temporary', 'recoverable', 'retry', 'pending', 'delayed'
            ]
        }

        self.severity_patterns = {
            'severe': [
                r'FATAL', r'CRITICAL', r'PANIC', r'EMERGENCY',
                r'!!!+', r'ERROR.*ERROR', r'SYSTEM.*DOWN'
            ],
            'medium': [
                r'ERROR', r'EXCEPTION', r'WARNING', r'FAILED',
                r'!!', r'\bFAIL\b', r'NULL.*POINTER'
            ],
            'mild': [
                r'INFO', r'DEBUG', r'NOTICE', r'WARN\b',
                r'!', r'retry', r'pending'
            ]
        }

    def analyze(self, error_message: str) -> str:
        """
        Analyze error message severity.

        Args:
            error_message: The error message to analyze

        Returns:
            Severity level: 'mild', 'medium', or 'severe'
        """
        if not error_message:
            return 'mild'

        message_lower = error_message.lower()

        # Calculate severity score
        score = 0

        # Check keywords
        for severity, keywords in self.severity_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    if severity == 'severe':
                        score += 3
                    elif severity == 'medium':
                        score += 2
                    else:
                        score += 1

        # Check patterns
        for severity, patterns in self.severity_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    if severity == 'severe':
                        score += 3
                    elif severity == 'medium':
                        score += 2
                    else:
                        score += 1

        # Count exclamation marks
        score += error_message.count('!') * 0.5
        score += error_message.count('!!!') * 2

        # Count uppercase words
        uppercase_words = len([w for w in error_message.split() if w.isupper() and len(w) > 2])
        score += uppercase_words * 0.5

        # Determine severity based on score
        if score >= 8:
            return 'severe'
        elif score >= 3:
            return 'medium'
        else:
            return 'mild'

    def get_severity_details(self, error_message: str) -> Dict[str, any]:
        """
        Get detailed severity analysis.

        Args:
            error_message: The error message to analyze

        Returns:
            Dictionary with severity details
        """
        severity = self.analyze(error_message)
        message_lower = error_message.lower()

        found_keywords = []
        for keywords in self.severity_keywords.values():
            for keyword in keywords:
                if keyword in message_lower:
                    found_keywords.append(keyword)

        return {
            'severity': severity,
            'found_keywords': found_keywords,
            'exclamation_count': error_message.count('!'),
            'uppercase_ratio': sum(1 for c in error_message if c.isupper()) / max(len(error_message), 1),
            'message_length': len(error_message)
        }
