"""
Main excuse generator module for CosmicExcuse.
"""

import random
import hashlib
import time
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from pathlib import Path

from cosmicexcuse.data.loader import DataLoader
from cosmicexcuse.analyzer import SeverityAnalyzer
from cosmicexcuse.markov import MarkovChain
from cosmicexcuse.formatter import ExcuseFormatter, HaikuFormatter
from cosmicexcuse.exceptions import LanguageNotSupportedError


@dataclass
class Excuse:
    """
    Represents a generated excuse with metadata.

    Attributes:
        text: The main excuse text
        recommendation: Suggested action to fix the issue
        severity: Detected severity level
        category: Primary excuse category used
        quality_score: Calculated quality score (0-100)
        quantum_probability: Random quantum probability
        language: Language code used
        timestamp: Generation timestamp
        metadata: Additional metadata
    """
    text: str
    recommendation: str
    severity: str
    category: str
    quality_score: int
    quantum_probability: float
    language: str
    timestamp: float
    metadata: Dict[str, Any]


class ExcuseGenerator:
    """
    Base excuse generator class.
    """

    SUPPORTED_LANGUAGES = ['en', 'bn']

    def __init__(self, language: str = 'en', data_path: Optional[Path] = None):
        """
        Initialize the excuse generator.

        Args:
            language: Language code ('en' for English, 'bn' for Bengali)
            data_path: Optional custom path to data directory

        Raises:
            LanguageNotSupportedError: If language is not supported
        """
        if language not in self.SUPPORTED_LANGUAGES:
            raise LanguageNotSupportedError(
                f"Language '{language}' not supported. "
                f"Supported languages: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )

        self.language = language
        self.data_loader = DataLoader(language, data_path)
        self.data = self.data_loader.load_all()

        self.analyzer = SeverityAnalyzer()
        self.markov = MarkovChain()
        self.formatter = ExcuseFormatter()

        # Build Markov chain from technical corpus
        self._build_markov_chain()

    def _build_markov_chain(self):
        """Build Markov chain from technical terms."""
        # Get technical terms from data
        technical_terms = []
        for category in ['quantum', 'technical', 'ai']:
            if category in self.data:
                technical_terms.extend(self.data[category])

        # Extract individual words and build corpus
        corpus = []
        for term in technical_terms:
            corpus.extend(term.split())

        self.markov.train(corpus)

    def generate(
            self,
            error_message: str = "",
            context: Optional[str] = None,
            category: Optional[str] = None
    ) -> Excuse:
        """
        Generate an excuse for the given error.

        Args:
            error_message: The error message to analyze
            context: Optional context about what was being done
            category: Optional specific category to use

        Returns:
            An Excuse object with the generated excuse and metadata
        """
        severity = self.analyzer.analyze(error_message)

        # Generate quantum seed for reproducible randomness
        quantum_seed = self._generate_quantum_seed(error_message)
        random.seed(quantum_seed)

        # Select categories
        if category and category in self.data:
            primary_category = category
        else:
            primary_category = random.choice(list(self.data.keys()))

        # Ensure we don't pick recommendations or connectors as primary
        while primary_category in ['recommendations', 'connectors', 'intensifiers']:
            primary_category = random.choice(list(self.data.keys()))

        # Get excuse components
        primary_excuse = random.choice(self.data[primary_category])

        # Get secondary category
        available_categories = [
            k for k in self.data.keys()
            if k not in [primary_category, 'recommendations', 'connectors', 'intensifiers']
        ]
        secondary_category = random.choice(available_categories)
        secondary_excuse = random.choice(self.data[secondary_category])

        # Get intensifier based on severity
        intensifier = self._get_intensifier(severity)

        # Get connector
        connector = random.choice(self.data.get('connectors', ['which caused']))

        # Generate Markov nonsense
        markov_phrase = self.markov.generate(length=5)

        # Construct the excuse
        excuse_text = self.formatter.format_excuse(
            primary_excuse=primary_excuse,
            secondary_excuse=secondary_excuse,
            intensifier=intensifier,
            connector=connector,
            markov_phrase=markov_phrase,
            severity=severity
        )

        # Get recommendation
        recommendation = random.choice(
            self.data.get('recommendations', ['Try turning it off and on again'])
        )

        # Calculate quality score
        quality_score = self._calculate_quality_score(excuse_text, quantum_seed)

        # Create Excuse object
        excuse = Excuse(
            text=excuse_text,
            recommendation=recommendation,
            severity=severity,
            category=primary_category,
            quality_score=quality_score,
            quantum_probability=random.random(),
            language=self.language,
            timestamp=time.time(),
            metadata={
                'secondary_category': secondary_category,
                'markov_component': markov_phrase,
                'context': context,
                'error_message': error_message
            }
        )

        return excuse

    def _generate_quantum_seed(self, error_message: str) -> int:
        """Generate a 'quantum' seed from the error message."""
        hash_input = f"{error_message}{time.time()}"
        hash_hex = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return int(hash_hex, 16)

    def _get_intensifier(self, severity: str) -> str:
        """Get an intensifier based on severity."""
        intensifiers = self.data.get('intensifiers', {})

        if isinstance(intensifiers, dict):
            severity_intensifiers = intensifiers.get(severity, ['definitely'])
        else:
            severity_intensifiers = ['definitely']

        return random.choice(severity_intensifiers)

    def _calculate_quality_score(self, excuse_text: str, seed: int) -> int:
        """Calculate a 'quality score' for the excuse."""
        # Completely arbitrary scoring algorithm
        score = len(excuse_text) * seed % 100

        # Bonus points for certain keywords
        bonus_words = ['quantum', 'cosmic', 'AI', 'blockchain', 'neural']
        for word in bonus_words:
            if word.lower() in excuse_text.lower():
                score = min(100, score + 5)

        return max(1, min(100, score))

    def generate_batch(self, count: int = 5) -> List[Excuse]:
        """
        Generate multiple excuses.

        Args:
            count: Number of excuses to generate

        Returns:
            List of Excuse objects
        """
        excuses = []

        # Sample error messages for variety
        sample_errors = [
            "FATAL ERROR: Everything is broken!",
            "SegmentationFault: Core dumped",
            "NullPointerException at line infinity",
            "KeyError: 'success'",
            "RuntimeError: Unknown error occurred",
            "ValueError: Invalid value",
            "TypeError: Type mismatch",
            "MemoryError: Out of memory",
        ]

        for _ in range(count):
            error = random.choice(sample_errors)
            excuse = self.generate(error)
            excuses.append(excuse)

        return excuses

    def generate_haiku(self, error_message: str = "") -> str:
        """
        Generate an excuse in haiku format.

        Args:
            error_message: Optional error message

        Returns:
            A haiku-formatted excuse string
        """
        haiku_formatter = HaikuFormatter()

        # Get components for haiku
        components = {
            'line_5_1': random.choice(self.data.get('quantum', ['Quantum states collapse'])),
            'line_7': random.choice(self.data.get('cosmic', ['The cosmos interferes today'])),
            'line_5_2': random.choice(self.data.get('ai', ['AI has gone rogue'])),
        }

        return haiku_formatter.format_haiku(components)


class CosmicExcuse(ExcuseGenerator):
    """
    Main public interface for CosmicExcuse package.
    Extends ExcuseGenerator with additional convenience methods.
    """

    def __init__(self, language: str = 'en', data_path: Optional[Path] = None):
        """
        Initialize CosmicExcuse generator.

        Args:
            language: Language code ('en' or 'bn')
            data_path: Optional custom data path

        Example:
            >>> generator = CosmicExcuse()
            >>> excuse = generator.generate("Database error")
            >>> print(excuse.text)
        """
        super().__init__(language, data_path)
        self.history: List[Excuse] = []

    def generate(
            self,
            error_message: str = "",
            context: Optional[str] = None,
            category: Optional[str] = None,
            save_history: bool = True
    ) -> Excuse:
        """
        Generate an excuse and optionally save to history.

        Args:
            error_message: The error to generate excuse for
            context: Optional context
            category: Optional category preference
            save_history: Whether to save to history

        Returns:
            Generated Excuse object
        """
        excuse = super().generate(error_message, context, category)

        if save_history:
            self.history.append(excuse)

        return excuse

    def get_best_excuse(self) -> Optional[Excuse]:
        """
        Get the highest quality excuse from history.

        Returns:
            Best Excuse object or None if no history
        """
        if not self.history:
            return None

        return max(self.history, key=lambda x: x.quality_score)

    def clear_history(self):
        """Clear the excuse history."""
        self.history.clear()

    def export_history(self, format: str = 'json') -> Union[str, List[Dict]]:
        """
        Export history in specified format.

        Args:
            format: Export format ('json' or 'text')

        Returns:
            Formatted history
        """
        if format == 'json':
            return [
                {
                    'text': exc.text,
                    'recommendation': exc.recommendation,
                    'severity': exc.severity,
                    'category': exc.category,
                    'quality_score': exc.quality_score,
                    'timestamp': exc.timestamp,
                    'language': exc.language
                }
                for exc in self.history
            ]
        elif format == 'text':
            return '\n\n'.join([
                f"Excuse #{i + 1} (Score: {exc.quality_score}/100):\n"
                f"{exc.text}\n"
                f"Recommendation: {exc.recommendation}"
                for i, exc in enumerate(self.history)
            ])
        else:
            raise ValueError(f"Unsupported format: {format}")
