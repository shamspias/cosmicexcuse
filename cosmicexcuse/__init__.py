"""
CosmicExcuse - Generate quantum-grade excuses for your code failures
=====================================================================

A professional excuse generator that uses AI techniques to create
plausible-sounding technical excuses for when your code doesn't work.

Basic Usage:
    >>> from cosmicexcuse import CosmicExcuse
    >>> generator = CosmicExcuse()
    >>> excuse = generator.generate("FATAL ERROR: Database crashed!")
    >>> print(excuse.text)

Multi-language Support:
    >>> generator = CosmicExcuse(language='bn')  # Bengali
    >>> excuse = generator.generate("ERROR!")

Author: Shamsuddin Ahmed
License: MIT
"""

from cosmicexcuse.__version__ import __version__
from cosmicexcuse.analyzer import SeverityAnalyzer
from cosmicexcuse.exceptions import (
    CosmicExcuseError,
    DataLoadError,
    LanguageNotSupportedError,
)
from cosmicexcuse.formatter import ExcuseFormatter, HaikuFormatter
from cosmicexcuse.generator import CosmicExcuse, ExcuseGenerator
from cosmicexcuse.leaderboard import ExcuseLeaderboard
from cosmicexcuse.markov import MarkovChain

__all__ = [
    "__version__",
    "CosmicExcuse",
    "ExcuseGenerator",
    "SeverityAnalyzer",
    "MarkovChain",
    "ExcuseFormatter",
    "HaikuFormatter",
    "ExcuseLeaderboard",
    "CosmicExcuseError",
    "LanguageNotSupportedError",
    "DataLoadError",
]


# Convenience function for quick usage
def generate(error_message: str = "", language: str = "en") -> str:
    """
    Quick function to generate an excuse without instantiating a class.

    Args:
        error_message: The error message to analyze
        language: Language code ('en' or 'bn')

    Returns:
        A string containing the generated excuse

    Example:
        >>> import cosmicexcuse
        >>> print(cosmicexcuse.generate("Segmentation fault"))
    """
    generator = CosmicExcuse(language=language)
    excuse = generator.generate(error_message)
    return excuse.text
