"""
Main excuse generator module for CosmicExcuse.
"""

import hashlib
import itertools
import os
import random
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from cosmicexcuse.analyzer import SeverityAnalyzer
from cosmicexcuse.data.loader import DataLoader
from cosmicexcuse.exceptions import LanguageNotSupportedError
from cosmicexcuse.formatter import ExcuseFormatter, HaikuFormatter
from cosmicexcuse.markov import MarkovChain


@dataclass
class Excuse:
    """
    Represents a generated excuse with metadata.
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


# Monotonic counter to guarantee changing seeds across rapid calls
_SEED_COUNTER = itertools.count()


class ExcuseGenerator:
    """
    Base excuse generator class.
    """

    SUPPORTED_LANGUAGES = ["en", "bn"]

    def __init__(self, language: str = "en", data_path: Optional[Path] = None):
        """
        Initialize the excuse generator.
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
        technical_terms: List[str] = []
        for category in ["quantum", "technical", "ai"]:
            if category in self.data:
                technical_terms.extend(self.data[category])

        corpus: List[str] = []
        for term in technical_terms:
            corpus.extend(term.split())

        self.markov.train(corpus)

    def generate(
        self,
        error_message: str = "",
        context: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Excuse:
        """
        Generate an excuse for the given error.
        """
        severity = self.analyzer.analyze(error_message)

        # High-entropy seed used only for scoring/metadata; do NOT reseed RNG
        quantum_seed = self._generate_quantum_seed(error_message)

        # Select categories using module-level random.choice (so tests can patch it)
        if category and category in self.data:
            primary_category = category
        else:
            primary_category = random.choice(list(self.data.keys()))

        # Ensure we don't pick recommendations or connectors as primary
        while primary_category in ["recommendations", "connectors", "intensifiers"]:
            primary_category = random.choice(list(self.data.keys()))

        # Get excuse components
        primary_excuse = random.choice(self.data[primary_category])

        # Get secondary category
        available_categories = [
            k
            for k in self.data.keys()
            if k
            not in [primary_category, "recommendations", "connectors", "intensifiers"]
        ]
        secondary_category = random.choice(available_categories)
        secondary_excuse = random.choice(self.data[secondary_category])

        # Get intensifier based on severity
        intensifier = self._get_intensifier(severity)

        # Get connector
        connector = random.choice(self.data.get("connectors", ["which caused"]))

        # Generate Markov nonsense
        markov_phrase = self.markov.generate(length=5)

        # Construct the excuse
        excuse_text = self.formatter.format_excuse(
            primary_excuse=primary_excuse,
            secondary_excuse=secondary_excuse,
            intensifier=intensifier,
            connector=connector,
            markov_phrase=markov_phrase,
            severity=severity,
        )

        # Get recommendation
        recommendation = random.choice(
            self.data.get("recommendations", ["Try turning it off and on again"])
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
                "secondary_category": secondary_category,
                "markov_component": markov_phrase,
                "context": context,
                "error_message": error_message,
            },
        )

        return excuse

    def _generate_quantum_seed(self, error_message: str) -> int:
        """
        Generate a high-entropy 64-bit seed that changes on every call,
        even when invoked multiple times within the same OS clock tick.
        """
        t1 = time.time_ns()
        t2 = time.perf_counter_ns()  # monotonic, high-res
        pid = os.getpid()
        tid = threading.get_ident()
        ctr = next(_SEED_COUNTER)
        h = hashlib.blake2b(digest_size=8)
        h.update(f"{error_message}|{t1}|{t2}|{pid}|{tid}|{ctr}".encode("utf-8"))
        return int.from_bytes(h.digest(), "big")

    def _get_intensifier(self, severity: str) -> str:
        """Get an intensifier based on severity."""
        intensifiers = self.data.get("intensifiers", {})

        if isinstance(intensifiers, dict):
            severity_intensifiers = intensifiers.get(severity, ["definitely"])
        else:
            severity_intensifiers = ["definitely"]

        return random.choice(severity_intensifiers)

    def _calculate_quality_score(self, excuse_text: str, seed: int) -> int:
        """Calculate a 'quality score' for the excuse."""
        score = len(excuse_text) * seed % 100

        bonus_words = ["quantum", "cosmic", "AI", "blockchain", "neural"]
        for word in bonus_words:
            if word.lower() in excuse_text.lower():
                score = min(100, score + 5)

        return max(1, min(100, score))

    def generate_batch(self, count: int = 5) -> List[Excuse]:
        """
        Generate multiple excuses, ensuring textual uniqueness.
        """
        excuses: List[Excuse] = []
        seen: set[str] = set()

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

        attempts = 0
        max_attempts = count * 10
        while len(excuses) < count and attempts < max_attempts:
            error = random.choice(sample_errors)
            excuse = self.generate(error)
            if excuse.text not in seen:
                seen.add(excuse.text)
                excuses.append(excuse)
            attempts += 1

        return excuses

    def generate_haiku(self, error_message: str = "") -> str:
        """
        Generate an excuse in haiku format.
        """
        haiku_formatter = HaikuFormatter()

        components = {
            "line_5_1": random.choice(
                self.data.get("quantum", ["Quantum states collapse"])
            ),
            "line_7": random.choice(
                self.data.get("cosmic", ["The cosmos interferes today"])
            ),
            "line_5_2": random.choice(self.data.get("ai", ["AI has gone rogue"])),
        }

        return haiku_formatter.format_haiku(components)


class CosmicExcuse(ExcuseGenerator):
    """
    Main public interface for CosmicExcuse package.
    Extends ExcuseGenerator with additional convenience methods.
    """

    def __init__(self, language: str = "en", data_path: Optional[Path] = None):
        super().__init__(language, data_path)
        self.history: List[Excuse] = []

    def generate(
        self,
        error_message: str = "",
        context: Optional[str] = None,
        category: Optional[str] = None,
        save_history: bool = True,
    ) -> Excuse:
        """Generate an excuse and optionally save to history."""
        excuse = super().generate(error_message, context, category)
        if save_history:
            self.history.append(excuse)
        return excuse

    def get_best_excuse(self) -> Optional[Excuse]:
        """Get the highest quality excuse from history."""
        if not self.history:
            return None
        return max(self.history, key=lambda x: x.quality_score)

    def clear_history(self):
        """Clear the excuse history."""
        self.history.clear()

    def export_history(self, format: str = "json") -> Union[str, List[Dict]]:
        """Export history in specified format."""
        if format == "json":
            return [
                {
                    "text": exc.text,
                    "recommendation": exc.recommendation,
                    "severity": exc.severity,
                    "category": exc.category,
                    "quality_score": exc.quality_score,
                    "timestamp": exc.timestamp,
                    "language": exc.language,
                }
                for exc in self.history
            ]
        elif format == "text":
            return "\n\n".join(
                [
                    f"Excuse #{i + 1} (Score: {exc.quality_score}/100):\n"
                    f"{exc.text}\n"
                    f"Recommendation: {exc.recommendation}"
                    for i, exc in enumerate(self.history)
                ]
            )
        else:
            raise ValueError(f"Unsupported format: {format}")
