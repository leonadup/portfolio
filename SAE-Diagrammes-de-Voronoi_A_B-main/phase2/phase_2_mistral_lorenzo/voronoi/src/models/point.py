import math

class Point:
    """Représente un point 2D avec des coordonnées x et y."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: 'Point') -> float:
        """Calcule la distance euclidienne entre deux points."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
