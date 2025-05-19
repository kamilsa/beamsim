"""
Random number generation utilities for the BEAMSim discrete-event simulation engine.

This module defines the RandomGenerator class, which provides methods
for generating random numbers with consistent seeding for reproducibility.
"""

import random


class RandomGenerator:
    """
    A class for generating random numbers with consistent seeding.
    """

    def __init__(self, seed):
        """
        Initialize the random generator with a seed.

        Args:
            seed (int): The seed for the random number generator.
        """
        self.seed = seed
        self.random_instance = random.Random(seed)

    def randint(self, a, b):
        """
        Generate a random integer between a and b (inclusive).

        Args:
            a (int): The lower bound.
            b (int): The upper bound.

        Returns:
            int: A random integer between a and b.
        """
        return self.random_instance.randint(a, b)

    def uniform(self, a, b):
        """
        Generate a random float between a and b.

        Args:
            a (float): The lower bound.
            b (float): The upper bound.

        Returns:
            float: A random float between a and b.
        """
        return self.random_instance.uniform(a, b)

    def choice(self, seq):
        """
        Select a random element from a sequence.

        Args:
            seq (list): The sequence to choose from.

        Returns:
            Any: A random element from the sequence.
        """
        return self.random_instance.choice(seq)

    def shuffle(self, seq):
        """
        Shuffle a sequence in place.

        Args:
            seq (list): The sequence to shuffle.
        """
        self.random_instance.shuffle(seq)

    def sample(self, population, k):
        """
        Select k unique random elements from a population.

        Args:
            population (list): The population to sample from.
            k (int): The number of elements to sample.

        Returns:
            list: A list of k unique random elements.
        """
        return self.random_instance.sample(population, k)