"""
Excuse formatting module for different output formats.
"""

import random
import textwrap
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseFormatter(ABC):
    """Abstract base class for formatters."""

    @abstractmethod
    def format(self, data: Dict[str, Any]) -> str:
        """Format the data into a string."""
        pass


class ExcuseFormatter(BaseFormatter):
    """
    Standard excuse formatter.
    """

    def __init__(self, max_length: Optional[int] = None):
        """
        Initialize the formatter.

        Args:
            max_length: Optional maximum length for the excuse
        """
        self.max_length = max_length

    def format(self, data: Dict[str, Any]) -> str:
        """
        Format excuse components into a complete excuse.

        Args:
            data: Dictionary containing excuse components

        Returns:
            Formatted excuse string
        """
        return self.format_excuse(**data)

    def format_excuse(
        self,
        primary_excuse: str,
        secondary_excuse: str,
        intensifier: str,
        connector: str,
        markov_phrase: str,
        severity: str,
        **kwargs,
    ) -> str:
        """
        Format components into an excuse string.

        Args:
            primary_excuse: Main excuse
            secondary_excuse: Secondary excuse
            intensifier: Severity intensifier
            connector: Connection phrase
            markov_phrase: Markov-generated technical phrase
            severity: Severity level
            **kwargs: Additional unused parameters

        Returns:
            Formatted excuse string
        """
        # Build the excuse
        excuse_parts = []

        # Main clause
        excuse_parts.append(f"The error was {intensifier} caused by {primary_excuse}")

        # Secondary clause
        excuse_parts.append(f"{connector} {secondary_excuse}")

        # Technical analysis
        if markov_phrase:
            excuse_parts.append(
                f"Additionally, analysis shows {markov_phrase} instability"
            )

        excuse = ". ".join(excuse_parts) + "."

        # Apply length limit if specified
        if self.max_length and len(excuse) > self.max_length:
            excuse = excuse[: self.max_length - 3] + "..."

        return excuse

    def format_technical(
        self, primary_excuse: str, technical_details: List[str], **kwargs
    ) -> str:
        """
        Format with technical details emphasis.

        Args:
            primary_excuse: Main excuse
            technical_details: List of technical details
            **kwargs: Additional parameters

        Returns:
            Technically-formatted excuse
        """
        details = " → ".join(technical_details[:3])
        return f"Technical Analysis: {primary_excuse} | Stack trace: {details}"

    def format_corporate(
        self, primary_excuse: str, recommendation: str, **kwargs
    ) -> str:
        """
        Format in corporate speak.

        Args:
            primary_excuse: Main excuse
            recommendation: Recommended action
            **kwargs: Additional parameters

        Returns:
            Corporate-formatted excuse
        """
        templates = [
            "We are currently experiencing {issue}. Our team is actively working on a resolution. {action}",
            "Due to {issue}, some users may experience degraded performance. {action}",
            "An unexpected {issue} has been identified. {action}",
            "We've detected {issue} affecting system stability. {action}",
        ]

        template = random.choice(templates)
        return template.format(issue=primary_excuse, action=recommendation)


class HaikuFormatter(BaseFormatter):
    """
    Format excuses as haikus.
    """

    def __init__(self):
        """Initialize haiku formatter."""
        self.syllable_5_templates = [
            "{excuse_short}",
            "Bits flip in the void",
            "Quantum states collapse",
            "The cache has failed us",
            "Cosmic rays strike hard",
            "AI has gone rogue",
            "Errors cascade down",
            "System cries for help",
            "Memory leaks out",
        ]

        self.syllable_7_templates = [
            "{excuse_medium}",
            "Digital tears fall like rain",
            "The servers are weeping now",
            "Kubernetes rebelling",
            "Distributed chaos reigns here",
            "The blockchain awakens now",
            "Neural networks dream of bugs",
            "Microservices conspire",
        ]

    def format(self, data: Dict[str, Any]) -> str:
        """
        Format data as haiku.

        Args:
            data: Dictionary with excuse components

        Returns:
            Haiku string
        """
        return self.format_haiku(data)

    def format_haiku(self, components: Dict[str, Any]) -> str:
        """
        Format components into haiku.

        Args:
            components: Dictionary with haiku lines or excuse components

        Returns:
            Formatted haiku (5-7-5 syllables)
        """
        if "line_5_1" in components:
            # Direct haiku components provided
            line1 = self._truncate_to_syllables(components.get("line_5_1", ""), 5)
            line2 = self._truncate_to_syllables(components.get("line_7", ""), 7)
            line3 = self._truncate_to_syllables(components.get("line_5_2", ""), 5)
        else:
            # Generate from templates
            line1 = random.choice(self.syllable_5_templates)
            line2 = random.choice(self.syllable_7_templates)
            line3 = random.choice(self.syllable_5_templates)

            # Ensure we don't repeat lines
            while line3 == line1:
                line3 = random.choice(self.syllable_5_templates)

        return f"{line1}\n{line2}\n{line3}"

    def _truncate_to_syllables(self, text: str, syllables: int) -> str:
        """
        Truncate text to approximately match syllable count.

        Args:
            text: Text to truncate
            syllables: Target syllable count

        Returns:
            Truncated text
        """
        # Simplified: assume ~1.3 syllables per word on average
        words = text.split()
        target_words = max(1, int(syllables / 1.3))
        return " ".join(words[:target_words])


class MarkdownFormatter(BaseFormatter):
    """
    Format excuses in Markdown.
    """

    def format(self, data: Dict[str, Any]) -> str:
        """
        Format as Markdown.

        Args:
            data: Excuse data dictionary

        Returns:
            Markdown-formatted string
        """
        output = []

        # Title
        output.append("## 🚨 System Excuse Report\n")

        # Main excuse
        if "text" in data:
            output.append(f"**Primary Analysis:** {data['text']}\n")

        # Metadata section
        output.append("### 📊 Metadata\n")

        if "severity" in data:
            severity_emoji = {"mild": "🟢", "medium": "🟡", "severe": "🔴"}
            emoji = severity_emoji.get(data["severity"], "⚪")
            output.append(f"- **Severity:** {emoji} {data['severity'].capitalize()}")

        if "category" in data:
            output.append(f"- **Category:** {data['category'].capitalize()}")

        if "quality_score" in data:
            output.append(f"- **Quality Score:** {data['quality_score']}/100")

        if "quantum_probability" in data:
            output.append(
                f"- **Quantum Probability:** {data['quantum_probability']:.4f}"
            )

        # Recommendation
        if "recommendation" in data:
            output.append("\n### 💡 Recommended Action\n")
            output.append("> {data['recommendation']}")

        # Technical details
        if "metadata" in data and "markov_component" in data["metadata"]:
            output.append("\n### 🔬 Technical Analysis\n")
            output.append("```\n{data['metadata']['markov_component']}\n```")

        return "\n".join(output)


class JSONFormatter(BaseFormatter):
    """
    Format excuses as JSON.
    """

    def format(self, data: Dict[str, Any]) -> str:
        """
        Format as JSON string.

        Args:
            data: Excuse data

        Returns:
            JSON-formatted string
        """
        import json

        # Extract relevant fields
        output = {
            "excuse": data.get("text", ""),
            "recommendation": data.get("recommendation", ""),
            "severity": data.get("severity", "unknown"),
            "category": data.get("category", "general"),
            "quality_score": data.get("quality_score", 0),
            "quantum_probability": data.get("quantum_probability", 0.0),
            "timestamp": data.get("timestamp", 0),
            "language": data.get("language", "en"),
        }

        # Add metadata if present
        if "metadata" in data:
            output["technical_details"] = data["metadata"].get("markov_component", "")
            output["error_message"] = data["metadata"].get("error_message", "")

        return json.dumps(output, indent=2, ensure_ascii=False)


class PlainTextFormatter(BaseFormatter):
    """
    Simple plain text formatter.
    """

    def __init__(self, width: int = 80):
        """
        Initialize plain text formatter.

        Args:
            width: Line width for wrapping
        """
        self.width = width

    def format(self, data: Dict[str, Any]) -> str:
        """
        Format as plain text.

        Args:
            data: Excuse data

        Returns:
            Plain text string
        """
        lines = []

        # Header
        lines.append("=" * self.width)
        lines.append("SYSTEM EXCUSE REPORT".center(self.width))
        lines.append("=" * self.width)
        lines.append("")

        # Main excuse
        if "text" in data:
            wrapped = textwrap.fill(
                f"EXCUSE: {data['text']}", width=self.width, subsequent_indent="  "
            )
            lines.append(wrapped)
            lines.append("")

        # Recommendation
        if "recommendation" in data:
            wrapped = textwrap.fill(
                f"RECOMMENDATION: {data['recommendation']}",
                width=self.width,
                subsequent_indent="  ",
            )
            lines.append(wrapped)
            lines.append("")

        # Details
        if "severity" in data:
            lines.append(f"SEVERITY: {data['severity'].upper()}")

        if "category" in data:
            lines.append(f"CATEGORY: {data['category'].upper()}")

        if "quality_score" in data:
            lines.append(f"QUALITY: {data['quality_score']}/100")

        lines.append("")
        lines.append("=" * self.width)

        return "\n".join(lines)


class TwitterFormatter(BaseFormatter):
    """
    Format excuses for Twitter/X (character limit).
    """

    def __init__(self, max_chars: int = 280):
        """
        Initialize Twitter formatter.

        Args:
            max_chars: Maximum character limit
        """
        self.max_chars = max_chars

    def format(self, data: Dict[str, Any]) -> str:
        """
        Format for Twitter.

        Args:
            data: Excuse data

        Returns:
            Tweet-sized string
        """
        text = data.get("text", "")

        # Add hashtags
        hashtags = " #debugging #programming #excuses #quantum"

        # Calculate available space
        available = self.max_chars - len(hashtags) - 3  # -3 for "..."

        if len(text) <= available:
            return text + hashtags
        else:
            # Truncate and add ellipsis
            return text[:available] + "..." + hashtags
