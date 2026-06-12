"""
Module définissant la classe Edge pour représenter une arête du diagramme de Voronoï.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from .point import Point


@dataclass
class Edge:
    """
    Représente une arête du diagramme de Voronoï.
    
    Attributes:
        start (Optional[Point]): Point de départ de l'arête
        end (Optional[Point]): Point d'arrivée de l'arête
        site1 (Point): Premier site de Voronoï adjacent
        site2 (Point): Second site de Voronoï adjacent
        is_infinite (bool): True si l'arête s'étend à l'infini
    """
    start: Optional[Point]
    end: Optional[Point]
    site1: Point
    site2: Point
    is_infinite: bool = False
    
    def __post_init__(self) -> None:
        """Valide les données après l'initialisation."""
        if not isinstance(self.site1, Point) or not isinstance(self.site2, Point):
            raise TypeError("Les sites doivent être des instances de Point")
        
        if self.start is not None and not isinstance(self.start, Point):
            raise TypeError("start doit être un Point ou None")
            
        if self.end is not None and not isinstance(self.end, Point):
            raise TypeError("end doit être un Point ou None")
    
    def is_valid(self) -> bool:
        """
        Vérifie si l'arête est valide (a au moins une extrémité définie).
        
        Returns:
            bool: True si l'arête est valide
        """
        return self.start is not None or self.end is not None
    
    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Retourne la boîte englobante de l'arête.
        
        Returns:
            Tuple[float, float, float, float]: (x_min, x_max, y_min, y_max)
        """
        x_coords = []
        y_coords = []
        
        if self.start:
            x_coords.append(self.start.x)
            y_coords.append(self.start.y)
        if self.end:
            x_coords.append(self.end.x)
            y_coords.append(self.end.y)
            
        if not x_coords:
            return (0, 0, 0, 0)
            
        return (min(x_coords), max(x_coords), min(y_coords), max(y_coords))