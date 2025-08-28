"""
Markov chain text generator module.
"""

import random
from collections import defaultdict
from typing import Dict, List, Optional


class MarkovChain:
    """
    Simple Markov chain text generator for technical jargon.
    """

    def __init__(self, order: int = 1):
        """
        Initialize Markov chain generator.

        Args:
            order: The order of the Markov chain (default 1)
        """
        self.order = order
        self.chain: Dict[tuple, List[str]] = defaultdict(list)
        self.starters: List[tuple] = []

        # Default technical corpus
        self.default_corpus = """
        distributed systems consensus algorithm byzantine fault tolerance
        eventual consistency CAP theorem race condition deadlock mutex
        garbage collection memory leak stack overflow heap corruption
        cache miss branch prediction pipeline stall context switch
        virtual memory page fault segmentation violation kernel panic
        quantum supremacy neural architecture tensor flow gradient descent
        backpropagation activation function loss landscape optimization
        container orchestration service mesh circuit breaker load balancer
        microservice architecture event sourcing CQRS saga pattern
        blockchain immutable ledger smart contract proof of work
        machine learning deep learning reinforcement learning transfer
        natural language processing computer vision generative adversarial
        edge computing fog computing serverless lambda function
        kubernetes docker swarm container registry helm chart
        continuous integration continuous deployment infrastructure code
        test driven development behavior driven agile scrum kanban
        object oriented functional programming reactive streams
        asynchronous programming callback promise async await
        RESTful API GraphQL gRPC websocket protocol buffer
        SQL NoSQL ACID BASE CAP eventual consistency
        indexing sharding partitioning replication clustering
        encryption hashing salting JWT OAuth SAML SSO
        firewall VPN proxy reverse proxy CDN WAF DDoS
        monitoring logging tracing metrics alerting observability
        """

        # Build default chain
        self.train(self.default_corpus.split())

    def train(self, corpus: List[str]):
        """
        Train the Markov chain on a corpus.

        Args:
            corpus: List of words to train on
        """
        if len(corpus) < self.order + 1:
            return

        # Build chain
        for i in range(len(corpus) - self.order):
            key = tuple(corpus[i : i + self.order])
            value = corpus[i + self.order]
            self.chain[key].append(value)

            # Track potential starters
            if i == 0 or corpus[i][0].isupper():
                self.starters.append(key)

        # Ensure we have starters
        if not self.starters and self.chain:
            self.starters = list(self.chain.keys())

    def generate(self, length: int = 5, start_word: Optional[str] = None) -> str:
        """
        Generate text using the Markov chain.

        Args:
            length: Number of words to generate
            start_word: Optional starting word

        Returns:
            Generated text string
        """
        if not self.chain:
            return "technical difficulties"

        # Choose starting point
        if start_word:
            # Find keys that contain the start word
            matching_keys = [k for k in self.chain.keys() if start_word in k]
            if matching_keys:
                current = random.choice(matching_keys)
            else:
                current = (
                    random.choice(self.starters)
                    if self.starters
                    else random.choice(list(self.chain.keys()))
                )
        else:
            current = (
                random.choice(self.starters)
                if self.starters
                else random.choice(list(self.chain.keys()))
            )

        result = list(current)

        # Generate text
        for _ in range(length - self.order):
            if current in self.chain:
                next_word = random.choice(self.chain[current])
                result.append(next_word)

                # Update current key
                if self.order == 1:
                    current = (next_word,)
                else:
                    current = tuple(list(current)[1:] + [next_word])
            else:
                # Dead end, pick a new random key
                if self.chain:
                    current = random.choice(list(self.chain.keys()))
                else:
                    break

        return " ".join(result)

    def generate_sentence(self, min_length: int = 3, max_length: int = 10) -> str:
        """
        Generate a sentence-like phrase.

        Args:
            min_length: Minimum number of words
            max_length: Maximum number of words

        Returns:
            Generated sentence
        """
        length = random.randint(min_length, max_length)
        return self.generate(length)

    def add_corpus(self, text: str):
        """
        Add additional text to the corpus.

        Args:
            text: Text to add to the corpus
        """
        words = text.split()
        self.train(words)

    def reset(self):
        """Reset the Markov chain."""
        self.chain.clear()
        self.starters.clear()

        # Rebuild with default corpus
        self.train(self.default_corpus.split())
