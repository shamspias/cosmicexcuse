"""Tests for Markov chain module."""

import pytest

from cosmicexcuse.markov import MarkovChain


class TestMarkovChain:
    """Test MarkovChain class."""

    def test_initialization(self):
        """Test Markov chain initialization."""
        markov = MarkovChain()
        assert markov.order == 1
        assert markov.chain is not None

    def test_train(self):
        """Test training on corpus."""
        markov = MarkovChain()
        corpus = ["test", "data", "for", "training"]

        markov.train(corpus)
        assert len(markov.chain) > 0

    def test_generate(self):
        """Test text generation."""
        markov = MarkovChain()

        result = markov.generate(length=5)
        assert isinstance(result, str)
        words = result.split()
        assert len(words) >= 1  # At least some output

    def test_generate_with_start_word(self):
        """Test generation with start word."""
        markov = MarkovChain()

        result = markov.generate(length=5, start_word="quantum")
        assert isinstance(result, str)

    def test_generate_sentence(self):
        """Test sentence generation."""
        markov = MarkovChain()

        result = markov.generate_sentence(min_length=3, max_length=10)
        assert isinstance(result, str)

        word_count = len(result.split())
        assert word_count >= 1  # At least some output

    def test_reset(self):
        """Test resetting chain."""
        markov = MarkovChain()
        markov.add_corpus("additional data")

        markov.reset()
        # Should have default corpus
        assert len(markov.chain) > 0
