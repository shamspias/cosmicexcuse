"""
Error severity analyzer module.
"""

import re
from typing import Dict  # Removed unused List import


class SeverityAnalyzer:
    """
    Analyzes error messages to determine severity level.
    """

    def __init__(self):
        """Initialize the severity analyzer."""
        self.severity_keywords = {
            "severe": [
                "fatal",
                "critical",
                "crash",
                "panic",
                "doom",
                "catastrophic",
                "emergency",
                "disaster",
                "meltdown",
                "apocalypse",
                "dead",
                "explosion",
                "fire",
                "burning",
                "destroyed",
                "corrupted",
                "segmentation",
                "core dump",
                "kernel panic",
            ],
            "medium": [
                "error",
                "fail",
                "failed",
                "exception",
                "problem",
                "issue",
                "broken",
                "invalid",
                "denied",
                "refused",
                "timeout",
                "overflow",
                "leak",
                "violation",
                "conflict",
                "missing",
                "undefined",
                "null pointer",
                "not found",
            ],
            "mild": [
                "warning",
                "warn",
                "deprecated",
                "notice",
                "info",
                "debug",
                "trace",
                "minor",
                "slight",
                "temporary",
                "recoverable",
                "retry",
                "pending",
                "delayed",
                "obsolete",
                "legacy",
            ],
        }

        self.severity_patterns = {
            "severe": [
                r"FATAL",
                r"CRITICAL",
                r"PANIC",
                r"EMERGENCY",
                r"!!!+",
                r"SYSTEM.*DOWN",
                r"KERNEL.*PANIC",
                r"SEGMENTATION.*FAULT",
                r"CORE.*DUMP",
            ],
            "medium": [
                r"\bERROR\b",
                r"EXCEPTION",
                r"FAILED",
                r"!!",
                r"\bFAIL\b",
                r"NULL.*POINTER",
                r"STACK.*OVERFLOW",
                r"MEMORY.*LEAK",
            ],
            "mild": [
                r"\bWARN(ING)?\b",
                r"\bINFO\b",
                r"DEBUG",
                r"NOTICE",
                r"DEPRECATED",
                r"TRACE",
                r"\bretry",
                r"pending",
            ],
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
            return "mild"

        message_lower = error_message.lower()

        # Calculate severity score
        score = 0
        severity_found = None

        # Check patterns first (they are more specific)
        for severity, patterns in self.severity_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    if severity == "severe":
                        score += 5
                        severity_found = "severe"
                    elif severity == "medium":
                        score += 3
                        if not severity_found:
                            severity_found = "medium"
                    else:  # mild
                        score += 1
                        if not severity_found:
                            severity_found = "mild"

        # If pattern matched, prioritize that result
        if severity_found and score >= 5:
            return "severe"
        elif severity_found == "mild" and score <= 2:
            return "mild"

        # Check keywords
        for severity, keywords in self.severity_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    if severity == "severe":
                        score += 3
                    elif severity == "medium":
                        score += 2
                    else:  # mild
                        score += 1

        # Count exclamation marks
        exclamation_count = error_message.count("!")
        if exclamation_count >= 3:
            score += 3
        elif exclamation_count >= 2:
            score += 2
        elif exclamation_count >= 1:
            score += 1

        # Count uppercase words (excluding common acronyms)
        words = error_message.split()
        uppercase_words = len(
            [
                w
                for w in words
                if w.isupper()
                and len(w) > 2
                and w not in ["CPU", "RAM", "API", "URL", "ID"]
            ]
        )
        score += uppercase_words * 0.5

        # Determine severity based on score
        if score >= 8:
            return "severe"
        elif score >= 4:
            return "medium"
        else:
            return "mild"

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

        found_patterns = []
        for patterns in self.severity_patterns.values():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    found_patterns.append(pattern)

        return {
            "severity": severity,
            "found_keywords": found_keywords,
            "found_patterns": found_patterns,
            "exclamation_count": error_message.count("!"),
            "uppercase_ratio": sum(1 for c in error_message if c.isupper())
            / max(len(error_message), 1),
            "message_length": len(error_message),
        }