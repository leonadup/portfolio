"""
Module définissant la classe Point.

Ce module contient la représentation d'un point dans un espace 2D,
élément fondamental du diagramme de Voronoï.
"""

import math
from typing import Tuple


class Point:
    """
    Représente un point dans un espace 2D.
    
    Cette classe est immuable et fournit des opérations géométriques
    de base nécessaires au calcul du diagramme de Voronoï.
    
    Attributes:
        x (float): Coordonnée x du point.
        y (float): Coordonnée y du point.
    """
    
    def __init__(self, x: float, y: float) -> None:
        """
        Initialise un point avec ses coordonnées.
        
        Args:
            x: Coordonnée x du point.
            y: Coordonnée y du point.
            
        Raises:
            TypeError: Si x ou y ne sont pas des nombres.
            ValueError: Si x ou y sont NaN ou infinis.
        """
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Les coordonnées doivent être des nombres")
        
        if math.isnan(x) or math.isnan(y) or math.isinf(x) or math.isinf(y):
            raise ValueError("Les coordonnées ne peuvent pas être NaN ou infinies")
        
        self._x = float(x)
        self._y = float(y)
    
    @property
    def x(self) -> float:
        """Retourne la coordonnée x du point."""
        return self._x
    
    @property
    def y(self) -> float:
        """Retourne la coordonnée y du point."""
        return self._y
    
    def distance_to(self, other: 'Point') -> float:
        """
        Calcule la distance euclidienne vers un autre point.
        
        Args:
            other: L'autre point vers lequel calculer la distance.
            
        Returns:
            La distance euclidienne entre les deux points.
            
        Raises:
            TypeError: Si other n'est pas un Point.
        """
        if not isinstance(other, Point):
            raise TypeError("L'argument doit être un Point")
        
        dx = self._x - other._x
        dy = self._y - other._y
        return math.sqrt(dx * dx + dy * dy)
    
    def squared_distance_to(self, other: 'Point') -> float:
        """
        Calcule le carré de la distance euclidienne vers un autre point.
        
        Cette méthode est plus rapide que distance_to car elle évite
        le calcul de la racine carrée, utile pour les comparaisons.
        
        Args:
            other: L'autre point vers lequel calculer la distance.
            
        Returns:
            Le carré de la distance euclidienne entre les deux points.
            
        Raises:
            TypeError: Si other n'est pas un Point.
        """
        if not isinstance(other, Point):
            raise TypeError("L'argument doit être un Point")
        
        dx = self._x - other._x
        dy = self._y - other._y
        return dx * dx + dy * dy
    
    def to_tuple(self) -> Tuple[float, float]:
        """
        Retourne les coordonnées sous forme de tuple.
        
        Returns:
            Un tuple (x, y) contenant les coordonnées du point.
        """
        return (self._x, self._y)
    
    def __eq__(self, other: object) -> bool:
        """
        Teste l'égalité entre deux points.
        
        Deux points sont égaux s'ils ont les mêmes coordonnées
        avec une tolérance de 1e-9.
        
        Args:
            other: L'objet à comparer.
            
        Returns:
            True si les points sont égaux, False sinon.
        """
        if not isinstance(other, Point):
            return False
        
        epsilon = 1e-9
        return (abs(self._x - other._x) < epsilon and 
                abs(self._y - other._y) < epsilon)
    
    def __hash__(self) -> int:
        """
        Retourne le hash du point.
        
        Returns:
            Hash basé sur les coordonnées arrondies.
        """
        return hash((round(self._x, 9), round(self._y, 9)))
    
    def __repr__(self) -> str:
        """
        Retourne une représentation string du point.
        
        Returns:
            Une chaîne représentant le point.
        """
        return f"Point({self._x}, {self._y})"
    
    def __str__(self) -> str:
        """
        Retourne une représentation string lisible du point.
        
        Returns:
            Une chaîne formatée avec les coordonnées.
        """
        return f"({self._x:.2f}, {self._y:.2f})"
    
    def __lt__(self, other: 'Point') -> bool:
        """
        Compare deux points pour le tri.
        
        Le tri se fait d'abord sur y, puis sur x si y est égal.
        Utile pour l'algorithme de Fortune.
        
        Args:
            other: L'autre point à comparer.
            
        Returns:
            True si ce point est "inférieur" à l'autre.
            
        Raises:
            TypeError: Si other n'est pas un Point.
        """
        if not isinstance(other, Point):
            raise TypeError("Impossible de comparer un Point avec un autre type")
        
        epsilon = 1e-9
        if abs(self._y - other._y) > epsilon:
            return self._y < other._y
        return self._x < other._x