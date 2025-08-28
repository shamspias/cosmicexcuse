"""Tests for the severity analyzer module."""

import pytest

from cosmicexcuse.analyzer import SeverityAnalyzer


class TestSeverityAnalyzer:
    """Test SeverityAnalyzer class."""

    def test_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.severity_keywords is not None
        assert analyzer.severity_patterns is not None

    def test_analyze_empty_message(self, analyzer):
        """Test analyzing empty message."""
        assert analyzer.analyze("") == "mild"

    def test_analyze_mild_errors(self, analyzer):
        """Test mild error detection."""
        mild_errors = [
            "Warning: deprecated function",
            "INFO: Processing started",
            "Debug: Variable value is 5",
            "Notice: Configuration updated",
        ]

        for error in mild_errors:
            assert analyzer.analyze(error) == "mild"

    def test_analyze_medium_errors(self, analyzer):
        """Test medium error detection."""
        medium_errors = [
            "ERROR: Connection failed",
            "Exception: Invalid input",
            "Failed to load resource",
            "Null pointer detected",
        ]

        for error in medium_errors:
            severity = analyzer.analyze(error)
            assert severity in ["medium", "severe"]  # Some might escalate

    def test_analyze_severe_errors(self, analyzer):
        """Test severe error detection."""
        severe_errors = [
            "FATAL ERROR: System crash!!!",
            "CRITICAL: Database corrupted",
            "PANIC: Kernel panic detected",
            "Segmentation fault (core dumped)",
        ]

        for error in severe_errors:
            assert analyzer.analyze(error) == "severe"

    def test_get_severity_details(self, analyzer):
        """Test getting detailed severity analysis."""
        error = "FATAL ERROR: System crash!!!"
        details = analyzer.get_severity_details(error)

        assert details["severity"] == "severe"
        assert details["exclamation_count"] == 3
        assert "found_keywords" in details
        assert "found_patterns" in details
