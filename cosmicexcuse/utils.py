"""
Utility functions for CosmicExcuse.
"""

import hashlib
import random
import re
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def generate_seed(input_string: str, salt: Optional[str] = None) -> int:
    """
    Generate a deterministic seed from input string.

    Args:
        input_string: Input string to generate seed from
        salt: Optional salt for additional randomness

    Returns:
        Integer seed value
    """
    if salt:
        input_string = f"{input_string}{salt}"
    else:
        input_string = f"{input_string}{time.time()}"

    hash_hex = hashlib.md5(input_string.encode()).hexdigest()
    return int(hash_hex[:8], 16)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    return text[: max_length - len(suffix)] + suffix


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text.

    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length

    Returns:
        List of keywords
    """
    # Remove special characters and split
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    # Filter by length and remove common words
    common_words = {
        "the",
        "and",
        "for",
        "are",
        "but",
        "not",
        "you",
        "all",
        "was",
        "were",
        "been",
        "have",
        "has",
        "had",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "can",
        "this",
        "that",
        "these",
        "those",
        "with",
        "from",
    }

    keywords = [
        word for word in words if len(word) >= min_length and word not in common_words
    ]

    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)

    return unique_keywords


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts (0-1).

    Args:
        text1: First text
        text2: Second text

    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0

    # Extract keywords from both texts
    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))

    if not keywords1 and not keywords2:
        return 1.0 if text1 == text2 else 0.0

    if not keywords1 or not keywords2:
        return 0.0

    # Calculate Jaccard similarity
    intersection = keywords1.intersection(keywords2)
    union = keywords1.union(keywords2)

    return len(intersection) / len(union)


def format_timestamp(timestamp: float, format: str = "human") -> str:
    """
    Format timestamp for display.

    Args:
        timestamp: Unix timestamp
        format: Format type ('human', 'iso', 'relative')

    Returns:
        Formatted timestamp string
    """
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)

    if format == "iso":
        return dt.isoformat()

    elif format == "relative":
        now = datetime.now(timezone.utc)
        delta = now - dt

        if delta.days > 365:
            return f"{delta.days // 365} year{'s' if delta.days // 365 > 1 else ''} ago"
        elif delta.days > 30:
            return f"{delta.days // 30} month{'s' if delta.days // 30 > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hour{'s' if delta.seconds // 3600 > 1 else ''} ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60} minute{'s' if delta.seconds // 60 > 1 else ''} ago"
        else:
            return "just now"

    else:  # human format
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def weighted_choice(choices: Dict[Any, float]) -> Any:
    """
    Make a weighted random choice.

    Args:
        choices: Dictionary mapping choices to weights

    Returns:
        Selected choice
    """
    if not choices:
        return None

    total = sum(choices.values())
    if total <= 0:
        return random.choice(list(choices.keys()))

    r = random.uniform(0, total)
    upto = 0

    for choice, weight in choices.items():
        if upto + weight >= r:
            return choice
        upto += weight

    return random.choice(list(choices.keys()))


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input.

    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove control characters
    text = "".join(char for char in text if char.isprintable() or char.isspace())

    # Normalize whitespace
    text = " ".join(text.split())

    # Truncate if necessary
    text = truncate_text(text, max_length, "")

    return text.strip()


def parse_error_code(error_message: str) -> Optional[Tuple[str, str]]:
    """
    Try to parse error code and type from message.

    Args:
        error_message: Error message to parse

    Returns:
        Tuple of (error_type, error_code) or None
    """
    patterns = [
        r"([A-Z][a-zA-Z]+Error)(?:\s*:\s*(.+))?",  # PythonError: message
        r"(ERROR)\s+(\d+)",  # ERROR 404
        r"([A-Z]+)-(\d+)",  # HTTP-500
        r"(0x[0-9A-Fa-f]+)",  # Hex error codes
        r"(\w+Exception)(?:\s*:\s*(.+))?",  # JavaException: message
    ]

    for pattern in patterns:
        match = re.search(pattern, error_message)
        if match:
            if len(match.groups()) == 2:
                return (match.group(1), match.group(2) or "")
            else:
                return (match.group(1), "")

    return None


def generate_error_id() -> str:
    """
    Generate a unique error ID.

    Returns:
        Unique error ID string
    """
    timestamp = int(time.time() * 1000)
    random_part = random.randint(1000, 9999)
    return f"ERR-{timestamp}-{random_part}"


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.

    Args:
        text: Text to split

    Returns:
        List of sentences
    """
    # Simple sentence splitter
    sentences = re.split(r"[.!?]+", text)
    return [s.strip() for s in sentences if s.strip()]


def is_valid_language_code(code: str) -> bool:
    """
    Check if language code is valid ISO 639-1.

    Args:
        code: Language code to check

    Returns:
        True if valid
    """
    return bool(re.match(r"^[a-z]{2}$", code.lower()))


def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """
    Estimate reading time in seconds.

    Args:
        text: Text to estimate reading time for
        wpm: Words per minute reading speed

    Returns:
        Estimated reading time in seconds
    """
    words = len(text.split())
    minutes = words / wpm
    return max(1, int(minutes * 60))


def create_progress_bar(current: int, total: int, length: int = 50) -> str:
    """
    Create ASCII progress bar.

    Args:
        current: Current progress value
        total: Total value
        length: Bar length in characters

    Returns:
        Progress bar string
    """
    if total <= 0:
        return "[" + "?" * length + "]"

    filled = int(length * current / total)
    bar = "█" * filled + "░" * (length - filled)
    percentage = (current / total) * 100

    return f"[{bar}] {percentage:.1f}%"


class RateLimiter:
    """Simple rate limiter implementation."""

    def __init__(self, max_calls: int, period: float):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: List[float] = []

    def is_allowed(self) -> bool:
        """
        Check if action is allowed.

        Returns:
            True if action is allowed
        """
        now = time.time()

        # Remove old calls outside the period
        self.calls = [t for t in self.calls if now - t < self.period]

        # Check if we can make another call
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True

        return False

    def reset(self):
        """Reset the rate limiter."""
        self.calls.clear()
