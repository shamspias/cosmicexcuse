"""Pytest configuration and fixtures."""

import json

import pytest

from cosmicexcuse import CosmicExcuse, ExcuseGenerator
from cosmicexcuse.analyzer import SeverityAnalyzer
from cosmicexcuse.leaderboard import ExcuseLeaderboard
from cosmicexcuse.markov import MarkovChain


@pytest.fixture
def generator():
    """Fixture for ExcuseGenerator."""
    return ExcuseGenerator()


@pytest.fixture
def cosmic():
    """Fixture for CosmicExcuse."""
    return CosmicExcuse()


@pytest.fixture
def analyzer():
    """Fixture for SeverityAnalyzer."""
    return SeverityAnalyzer()


@pytest.fixture
def markov():
    """Fixture for MarkovChain."""
    return MarkovChain()


@pytest.fixture
def leaderboard():
    """Fixture for ExcuseLeaderboard."""
    return ExcuseLeaderboard()


@pytest.fixture
def temp_data_path(tmp_path):
    """Create temporary data path for testing."""
    data_dir = tmp_path / "data" / "en"
    data_dir.mkdir(parents=True)

    # Create minimal test data
    test_data = {
        "category": "test",
        "language": "en",
        "version": "1.0.0",
        "excuses": ["test excuse 1", "test excuse 2"],
    }

    for category in [
        "quantum",
        "cosmic",
        "ai",
        "technical",
        "blame",
        "recommendations",
        "connectors",
    ]:
        with open(data_dir / f"{category}.json", "w") as f:
            json.dump(test_data, f)

    # Intensifiers need special structure
    intensifiers = {
        "mild": ["slightly"],
        "medium": ["definitely"],
        "severe": ["catastrophically"],
    }

    intensifiers_data = {
        "category": "intensifiers",
        "language": "en",
        "version": "1.0.0",
        "excuses": intensifiers,
    }

    with open(data_dir / "intensifiers.json", "w") as f:
        json.dump(intensifiers_data, f)

    return tmp_path / "data"
