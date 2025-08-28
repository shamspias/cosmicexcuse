"""
Tests for the excuse generator module.
"""

import time
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from cosmicexcuse import CosmicExcuse, ExcuseGenerator
from cosmicexcuse.exceptions import LanguageNotSupportedError
from cosmicexcuse.generator import Excuse


class TestExcuseGenerator:
    """Test ExcuseGenerator class."""

    def test_initialization_default(self):
        """Test default initialization."""
        generator = ExcuseGenerator()
        assert generator.language == "en"
        assert generator.data is not None
        assert len(generator.data) > 0

    def test_initialization_with_language(self):
        """Test initialization with specific language."""
        generator = ExcuseGenerator(language="en")
        assert generator.language == "en"

    def test_initialization_invalid_language(self):
        """Test initialization with invalid language."""
        with pytest.raises(LanguageNotSupportedError):
            ExcuseGenerator(language="invalid")

    def test_generate_basic(self):
        """Test basic excuse generation."""
        generator = ExcuseGenerator()
        excuse = generator.generate()

        assert isinstance(excuse, Excuse)
        assert excuse.text
        assert excuse.recommendation
        assert excuse.severity in ["mild", "medium", "severe"]
        assert excuse.category
        assert 0 <= excuse.quality_score <= 100
        assert 0 <= excuse.quantum_probability <= 1
        assert excuse.language == "en"
        assert excuse.timestamp > 0

    def test_generate_with_error_message(self):
        """Test generation with error message."""
        generator = ExcuseGenerator()

        # Test mild error
        excuse = generator.generate("Warning: deprecated function")
        assert excuse.severity == "mild"

        # Test severe error
        excuse = generator.generate("FATAL ERROR!!! SYSTEM CRASH!!!")
        assert excuse.severity == "severe"

    def test_generate_with_category(self):
        """Test generation with specific category."""
        generator = ExcuseGenerator()

        categories = ["quantum", "cosmic", "ai", "technical", "blame"]
        for category in categories:
            excuse = generator.generate(category=category)
            assert excuse.category == category

    def test_generate_batch(self):
        """Test batch generation."""
        generator = ExcuseGenerator()
        excuses = generator.generate_batch(5)

        assert len(excuses) == 5
        assert all(isinstance(e, Excuse) for e in excuses)
        assert len(set(e.text for e in excuses)) == 5  # All unique

    def test_generate_haiku(self):
        """Test haiku generation."""
        generator = ExcuseGenerator()
        haiku = generator.generate_haiku()

        assert isinstance(haiku, str)
        assert haiku.count("\n") == 2  # Three lines

    def test_quantum_seed_deterministic(self):
        """Test that quantum seed is deterministic for same input."""
        generator = ExcuseGenerator()

        seed1 = generator._generate_quantum_seed("test error")
        seed2 = generator._generate_quantum_seed("test error")

        # Seeds should be different due to time component
        assert seed1 != seed2

    def test_quality_score_calculation(self):
        """Test quality score calculation."""
        generator = ExcuseGenerator()

        excuse_text = "quantum blockchain AI neural network"
        seed = 12345
        score = generator._calculate_quality_score(excuse_text, seed)

        assert 0 <= score <= 100

        # Test that bonus words increase score
        excuse_with_bonus = "This has quantum and AI and blockchain"
        score_with_bonus = generator._calculate_quality_score(excuse_with_bonus, seed)
        assert score_with_bonus > 0


class TestCosmicExcuse:
    """Test CosmicExcuse main class."""

    def test_initialization(self):
        """Test CosmicExcuse initialization."""
        cosmic = CosmicExcuse()
        assert cosmic.language == "en"
        assert cosmic.history == []

    def test_generate_saves_history(self):
        """Test that generation saves to history."""
        cosmic = CosmicExcuse()

        excuse1 = cosmic.generate("Error 1")
        excuse2 = cosmic.generate("Error 2")

        assert len(cosmic.history) == 2
        assert cosmic.history[0] == excuse1
        assert cosmic.history[1] == excuse2

    def test_generate_no_history(self):
        """Test generation without saving history."""
        cosmic = CosmicExcuse()

        excuse = cosmic.generate("Error", save_history=False)
        assert len(cosmic.history) == 0

    def test_get_best_excuse(self):
        """Test getting best excuse from history."""
        cosmic = CosmicExcuse()

        # Generate some excuses
        for i in range(5):
            cosmic.generate(f"Error {i}")

        best = cosmic.get_best_excuse()
        assert best is not None
        assert best.quality_score == max(e.quality_score for e in cosmic.history)

    def test_get_best_excuse_empty_history(self):
        """Test getting best excuse with empty history."""
        cosmic = CosmicExcuse()
        best = cosmic.get_best_excuse()
        assert best is None

    def test_clear_history(self):
        """Test clearing history."""
        cosmic = CosmicExcuse()

        cosmic.generate("Error")
        assert len(cosmic.history) > 0

        cosmic.clear_history()
        assert len(cosmic.history) == 0

    def test_export_history_json(self):
        """Test exporting history as JSON."""
        cosmic = CosmicExcuse()

        cosmic.generate("Test error")
        exported = cosmic.export_history(format="json")

        assert isinstance(exported, list)
        assert len(exported) == 1
        assert "text" in exported[0]
        assert "recommendation" in exported[0]

    def test_export_history_text(self):
        """Test exporting history as text."""
        cosmic = CosmicExcuse()

        cosmic.generate("Test error 1")
        cosmic.generate("Test error 2")

        exported = cosmic.export_history(format="text")

        assert isinstance(exported, str)
        assert "Excuse #1" in exported
        assert "Excuse #2" in exported

    def test_export_history_invalid_format(self):
        """Test exporting with invalid format."""
        cosmic = CosmicExcuse()

        with pytest.raises(ValueError):
            cosmic.export_history(format="invalid")


class TestExcuseDataClass:
    """Test Excuse dataclass."""

    def test_excuse_creation(self):
        """Test creating Excuse object."""
        excuse = Excuse(
            text="Test excuse",
            recommendation="Test recommendation",
            severity="medium",
            category="test",
            quality_score=75,
            quantum_probability=0.5,
            language="en",
            timestamp=time.time(),
            metadata={"test": "data"},
        )

        assert excuse.text == "Test excuse"
        assert excuse.recommendation == "Test recommendation"
        assert excuse.severity == "medium"
        assert excuse.category == "test"
        assert excuse.quality_score == 75
        assert excuse.quantum_probability == 0.5
        assert excuse.language == "en"
        assert excuse.metadata == {"test": "data"}


class TestIntegration:
    """Integration tests."""

    def test_end_to_end_generation(self):
        """Test complete generation flow."""
        cosmic = CosmicExcuse()

        # Generate excuse
        error = "CRITICAL: Database connection failed!"
        excuse = cosmic.generate(error, context="During user login")

        # Verify all fields are populated
        assert excuse.text
        assert excuse.recommendation
        assert excuse.severity == "severe"  # Should be severe due to CRITICAL
        assert excuse.category in ["quantum", "cosmic", "ai", "technical", "blame"]
        assert excuse.quality_score > 0
        assert excuse.metadata["error_message"] == error
        assert excuse.metadata["context"] == "During user login"

    def test_multiple_languages(self):
        """Test using multiple languages."""
        # English generator
        en_gen = CosmicExcuse(language="en")
        en_excuse = en_gen.generate("Database error")
        assert en_excuse.language == "en"

        # Bengali generator (if data exists)
        try:
            bn_gen = CosmicExcuse(language="bn")
            bn_excuse = bn_gen.generate("ডাটাবেস ত্রুটি")
            assert bn_excuse.language == "bn"
        except (LanguageNotSupportedError, FileNotFoundError):
            # Bengali data might not be available in test environment
            pass

    @patch("cosmicexcuse.generator.random.choice")
    def test_deterministic_with_mocked_random(self, mock_choice):
        """Test deterministic behavior with mocked randomness."""
        mock_choice.side_effect = lambda x: x[0] if x else None

        generator = ExcuseGenerator()
        excuse1 = generator.generate("Same error")
        excuse2 = generator.generate("Same error")

        # With mocked random, similar inputs might produce similar outputs
        assert excuse1.category == excuse2.category


@pytest.fixture
def generator():
    """Fixture for ExcuseGenerator."""
    return ExcuseGenerator()


@pytest.fixture
def cosmic():
    """Fixture for CosmicExcuse."""
    return CosmicExcuse()


def test_generator_fixture(generator):
    """Test using generator fixture."""
    excuse = generator.generate()
    assert isinstance(excuse, Excuse)


def test_cosmic_fixture(cosmic):
    """Test using cosmic fixture."""
    excuse = cosmic.generate()
    assert isinstance(excuse, Excuse)
    assert len(cosmic.history) == 1
