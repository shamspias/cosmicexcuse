"""Tests for formatter module."""

import json

import pytest

from cosmicexcuse.formatter import (
    ExcuseFormatter,
    HaikuFormatter,
    JSONFormatter,
    MarkdownFormatter,
    PlainTextFormatter,
    TwitterFormatter,
)


class TestExcuseFormatter:
    """Test ExcuseFormatter class."""

    def test_basic_formatting(self):
        """Test basic excuse formatting."""
        formatter = ExcuseFormatter()

        result = formatter.format_excuse(
            primary_excuse="quantum interference",
            secondary_excuse="cosmic rays",
            intensifier="definitely",
            connector="which caused",
            markov_phrase="technical chaos",
            severity="medium",
        )

        assert "quantum interference" in result
        assert "cosmic rays" in result
        assert "definitely" in result

    def test_max_length(self):
        """Test formatting with max length."""
        formatter = ExcuseFormatter(max_length=50)

        long_excuse = "a" * 100
        result = formatter.format_excuse(
            primary_excuse=long_excuse,
            secondary_excuse="test",
            intensifier="very",
            connector="causing",
            markov_phrase="",
            severity="mild",
        )

        assert len(result) <= 50
        assert result.endswith("...")


class TestHaikuFormatter:
    """Test HaikuFormatter class."""

    def test_haiku_format(self):
        """Test haiku formatting."""
        formatter = HaikuFormatter()

        result = formatter.format_haiku({})

        lines = result.split("\n")
        assert len(lines) == 3


class TestMarkdownFormatter:
    """Test MarkdownFormatter class."""

    def test_markdown_format(self):
        """Test markdown formatting."""
        formatter = MarkdownFormatter()

        data = {
            "text": "Test excuse",
            "severity": "medium",
            "category": "quantum",
            "quality_score": 75,
            "recommendation": "Try again",
        }

        result = formatter.format(data)

        assert "## " in result  # Has headers
        assert "**" in result  # Has bold text
        assert "Test excuse" in result


class TestJSONFormatter:
    """Test JSONFormatter class."""

    def test_json_format(self):
        """Test JSON formatting."""
        formatter = JSONFormatter()

        data = {
            "text": "Test excuse",
            "severity": "mild",
            "category": "test",
            "quality_score": 50,
        }

        result = formatter.format(data)

        # Should be valid JSON
        parsed = json.loads(result)
        assert parsed["excuse"] == "Test excuse"
        assert parsed["severity"] == "mild"


class TestTwitterFormatter:
    """Test TwitterFormatter class."""

    def test_twitter_format(self):
        """Test Twitter formatting."""
        formatter = TwitterFormatter()

        long_text = "a" * 300
        result = formatter.format({"text": long_text})

        assert len(result) <= 280
        assert "#" in result  # Has hashtags
