"""
Error severity analyzer module.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Tuple


class SeverityAnalyzer:
    """
    Analyzes error messages to determine severity level.
    """

    def __init__(self) -> None:
        """Initialize the severity analyzer."""
        self.severity_keywords: Dict[str, List[str]] = {
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

        self.severity_patterns: Dict[str, List[str]] = {
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

        self._pattern_weights = {"severe": 5, "medium": 3, "mild": 1}
        self._keyword_weights = {"severe": 3, "medium": 2, "mild": 1}
        self._uppercase_exclusions = {"CPU", "RAM", "API", "URL", "ID"}

    # -------------------------
    # Public API
    # -------------------------

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

        msg_lower = error_message.lower()

        pattern_score, top_pattern = self._score_patterns(error_message)

        # Pattern priority short-circuits (preserve original behavior)
        if top_pattern == "severe" and pattern_score >= 5:
            return "severe"
        if top_pattern == "mild" and pattern_score <= 2:
            return "mild"

        total = 0.0
        total += pattern_score
        total += self._score_keywords(msg_lower)
        total += self._score_exclamations(error_message)
        total += self._score_uppercase(error_message)

        return self._score_to_severity(total)

    def get_severity_details(self, error_message: str) -> Dict[str, Any]:
        """
        Get detailed severity analysis.

        Args:
            error_message: The error message to analyze

        Returns:
            Dictionary with severity details
        """
        severity = self.analyze(error_message)
        msg_lower = error_message.lower()

        found_keywords = self._find_keywords(msg_lower)
        found_patterns = self._find_patterns(error_message)

        uppercase_ratio = sum(1 for c in error_message if c.isupper()) / max(
            len(error_message), 1
        )

        return {
            "severity": severity,
            "found_keywords": found_keywords,
            "found_patterns": found_patterns,
            "exclamation_count": error_message.count("!"),
            "uppercase_ratio": uppercase_ratio,
            "message_length": len(error_message),
        }

    # -------------------------
    # Internal helpers
    # -------------------------

    def _score_patterns(self, message: str) -> Tuple[int, str | None]:
        hits: List[Tuple[str, str]] = [
            (sev, pat)
            for sev, pats in self.severity_patterns.items()
            for pat in pats
            if re.search(pat, message, re.IGNORECASE)
        ]
        score = sum(self._pattern_weights[sev] for sev, _ in hits)
        top = self._pick_top_severity(sev for sev, _ in hits)
        return score, top

    def _score_keywords(self, msg_lower: str) -> int:
        return sum(
            self._keyword_weights[sev]
            for sev, kws in self.severity_keywords.items()
            for kw in kws
            if kw in msg_lower
        )

    @staticmethod
    def _score_exclamations(message: str) -> int:
        n = message.count("!")
        if n >= 3:
            return 3
        if n == 2:
            return 2
        if n == 1:
            return 1
        return 0

    def _score_uppercase(self, message: str) -> float:
        words = message.split()
        uppercase_words = [
            w
            for w in words
            if w.isupper() and len(w) > 2 and w not in self._uppercase_exclusions
        ]
        return len(uppercase_words) * 0.5

    @staticmethod
    def _score_to_severity(score: float) -> str:
        if score >= 8:
            return "severe"
        if score >= 4:
            return "medium"
        return "mild"

    def _find_keywords(self, msg_lower: str) -> List[str]:
        return [
            kw
            for kws in self.severity_keywords.values()
            for kw in kws
            if kw in msg_lower
        ]

    def _find_patterns(self, message: str) -> List[str]:
        return [
            pat
            for pats in self.severity_patterns.values()
            for pat in pats
            if re.search(pat, message, re.IGNORECASE)
        ]

    @staticmethod
    def _pick_top_severity(levels: Iterable[str]) -> str | None:
        order = {"mild": 0, "medium": 1, "severe": 2}
        top = -1
        top_sev = None
        for sev in levels:
            val = order.get(sev, -1)
            if val > top:
                top = val
                top_sev = sev
        return top_sev
