"""
Custom exceptions for CosmicExcuse package.
"""


class CosmicExcuseError(Exception):
    """Base exception for all CosmicExcuse errors."""

    pass


class LanguageNotSupportedError(CosmicExcuseError):
    """Raised when an unsupported language is requested."""

    pass


class DataLoadError(CosmicExcuseError):
    """Raised when data files cannot be loaded."""

    pass


class InvalidCategoryError(CosmicExcuseError):
    """Raised when an invalid category is specified."""

    pass


class MarkovChainError(CosmicExcuseError):
    """Raised when Markov chain generation fails."""

    pass


class FormatterError(CosmicExcuseError):
    """Raised when formatting fails."""

    pass
