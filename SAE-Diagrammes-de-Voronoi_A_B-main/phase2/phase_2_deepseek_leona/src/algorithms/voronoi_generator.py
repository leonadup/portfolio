"""
Module définissant l'interface pour les générateurs de diagrammes de Voronoï.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from src.models.point import Point
from src.models.edge import Edge


class VoronoiGenerator(ABC):
    """
    Interface abstraite pour les générateurs de diagrammes de Voronoï.
    
    Cette classe définit le contrat que tous les générateurs doivent respecter,
    conformément au principe d'interface ségrégation (SOLID).
    """
    
    @abstractmethod
    def generate(self, points: List[Point]) -> List[Edge]:
        """
        Génère le diagramme de Voronoï à partir d'une liste de points.
        
        Args:
            points: Liste des points (sites) pour lesquels générer le diagramme
            
        Returns:
            List[Edge]: Liste des arêtes du diagramme
            
        Raises:
            ValueError: Si la liste de points est vide ou contient moins de 2 points
        """
        pass
    
    @abstractmethod
    def get_bounding_box(self, points: List[Point]) -> Tuple[float, float, float, float]:
        """
        Calcule la boîte englobante des points.
        
        Args:
            points: Liste des points
            
        Returns:
            Tuple[float, float, float, float]: (x_min, x_max, y_min, y_max)
        """
        pass
    
    def validate_points(self, points: List[Point]) -> None:
        """
        Valide la liste de points.
        
        Args:
            points: Liste des points à valider
            
        Raises:
            ValueError: Si la validation échoue
        """
        if not points:
            raise ValueError("La liste de points ne peut pas être vide")
        
        if len(points) < 2:
            raise ValueError("Au moins 2 points sont nécessaires pour générer un diagramme")
        
        for point in points:
            if not isinstance(point, Point):
                raise TypeError("Tous les éléments doivent être des instances de Point")