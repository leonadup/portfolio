"""
Module définissant la classe Point pour représenter un point dans le plan.
"""

from dataclasses import dataclass
from typing import Union, Tuple
import math


@dataclass(frozen=True)
class Point:
    """
    Représente un point dans le plan cartésien.
    
    Attributes:
        x (float): Coordonnée x du point
        y (float): Coordonnée y du point
    
    La classe est immuable (frozen=True) pour garantir l'integrité des données.
    """
    x: float
    y: float
    
    def __post_init__(self) -> None:
        """Valide les coordonnées après l'initialisation."""
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            raise TypeError("Les coordonnées doivent être des nombres")
    
    def distance_to(self, other: 'Point') -> float:
        """
        Calcule la distance euclidienne jusqu'à un autre point.
        
        Args:
            other: L'autre point
            
        Returns:
            float: Distance entre les deux points
            
        Raises:
            TypeError: Si other n'est pas une instance de Point
        """
        if not isinstance(other, Point):
            raise TypeError("L'argument doit être un Point")
        
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convertit le point en tuple (x, y)."""
        return (self.x, self.y)
    
    def __repr__(self) -> str:
        """Représentation string du point."""
        return f"Point({self.x:.2f}, {self.y:.2f})"