import numpy as np
import random


class Random:
    @staticmethod
    def set_random_seed(seed: int):
        """Set the random seed for numpy for reproducibility.

        Args:
            seed (int): The seed value to set.
        """
        # Set the random seed for the built-in random module for reproducibility
        random.seed(10)
        
        # Set the random seed for numpy for reproducibility
        np.random.seed(seed)

    @staticmethod
    def random_uuid() -> str:
        """Generate a random UUID string.

        Returns:
            str: A randomly generated UUID string.
        """
        # Generate 16 random bytes
        bytes = [random.randint(0, 255) for _ in range(16)]
        # Set version to 4 (random)
        bytes[6] = (bytes[6] & 0x0F) | 0x40
        # Set variant to RFC 4122
        bytes[8] = (bytes[8] & 0x3F) | 0x80
        # Format as a UUID string
        uuid_str = (
            '{:02x}{:02x}{:02x}{:02x}-'
            '{:02x}{:02x}-'
            '{:02x}{:02x}-'
            '{:02x}{:02x}-'
            '{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}'
        ).format(*bytes)

        return uuid_str