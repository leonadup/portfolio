"""
Module contenant des utilitaires géométriques pour les calculs de Voronoï.
"""

import math
from typing import Tuple, Optional
from src.models.point import Point


class GeometryUtils:
    """
    Classe utilitaire pour les calculs géométriques.
    
    Cette classe contient des méthodes statiques pour les calculs
    nécessaires à l'algorithme de Fortune.
    """
    
    @staticmethod
    def calculate_circle_center(p1: Point, p2: Point, p3: Point) -> Optional[Point]:
        """
        Calcule le centre du cercle passant par trois points.
        
        Args:
            p1, p2, p3: Trois points non colinéaires
            
        Returns:
            Optional[Point]: Centre du cercle ou None si les points sont colinéaires
        """
        # Calcul des médiatrices
        mid_ab = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)
        mid_bc = Point((p2.x + p3.x) / 2, (p2.y + p3.y) / 2)
        
        # Pentes des médiatrices
        if p2.y != p1.y:
            slope_ab = -(p2.x - p1.x) / (p2.y - p1.y)
        else:
            slope_ab = float('inf')
            
        if p3.y != p2.y:
            slope_bc = -(p3.x - p2.x) / (p3.y - p2.y)
        else:
            slope_bc = float('inf')
        
        # Vérification de colinéarité
        # Calcul du déterminant pour vérifier si les points sont colinéaires
        det = (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)
        if abs(det) < 1e-10:
            return None  # Points colinéaires
        
        # Cas des pentes infinies (médiatrices verticales)
        if slope_ab == float('inf') and slope_bc == float('inf'):
            return None  # Points alignés verticalement
        
        if slope_ab == float('inf'):
            # Médiatrice AB verticale
            x = mid_ab.x
            y = slope_bc * (x - mid_bc.x) + mid_bc.y
        elif slope_bc == float('inf'):
            # Médiatrice BC verticale
            x = mid_bc.x
            y = slope_ab * (x - mid_ab.x) + mid_ab.y
        else:
            # Vérifier si les pentes sont égales (médiatrices parallèles)
            if abs(slope_ab - slope_bc) < 1e-10:
                return None  # Médiatrices parallèles -> points colinéaires
            
            # Intersection des deux médiatrices
            x = (slope_ab * mid_ab.x - slope_bc * mid_bc.x + mid_bc.y - mid_ab.y) / (slope_ab - slope_bc)
            y = slope_ab * (x - mid_ab.x) + mid_ab.y
        
        return Point(x, y)
    
    @staticmethod
    def is_point_in_circle(point: Point, center: Point, radius: float, epsilon: float = 1e-10) -> bool:
        """
        Vérifie si un point est à l'intérieur d'un cercle.
        
        Args:
            point: Point à tester
            center: Centre du cercle
            radius: Rayon du cercle
            epsilon: Tolérance pour les calculs flottants
            
        Returns:
            bool: True si le point est dans le cercle
        """
        distance_squared = (point.x - center.x) ** 2 + (point.y - center.y) ** 2
        return distance_squared <= radius ** 2 + epsilon
    
    @staticmethod
    def calculate_parabola_intersection(p1: Point, p2: Point, directrix_y: float) -> Tuple[float, float]:
        """
        Calcule l'intersection de deux paraboles ayant pour foyers p1 et p2
        et pour directrice la ligne horizontale y = directrix_y.
        
        Args:
            p1, p2: Les foyers des paraboles
            directrix_y: Position y de la directrice
            
        Returns:
            Tuple[float, float]: Les points d'intersection en x
        """
        # Cas particulier : si les deux points ont la même coordonnée y
        if abs(p1.y - p2.y) < 1e-10:
            # Même y - la médiatrice est verticale
            x = (p1.x + p2.x) / 2
            return (x, x)
        
        # Vérifier que la directrice n'est pas trop proche des foyers
        if abs(p1.y - directrix_y) < 1e-10 or abs(p2.y - directrix_y) < 1e-10:
            return (float('nan'), float('nan'))
        
        # Calcul des paramètres des paraboles
        a1 = 1 / (2 * (p1.y - directrix_y))
        a2 = 1 / (2 * (p2.y - directrix_y))
        
        # Si les paramètres sont trop proches (paraboles presque parallèles)
        if abs(a1 - a2) < 1e-10:
            return (float('inf'), float('inf'))
        
        # Résolution de l'équation quadratique
        b1 = -2 * p1.x * a1
        b2 = -2 * p2.x * a2
        c1 = a1 * (p1.x ** 2 + p1.y ** 2 - directrix_y ** 2)
        c2 = a2 * (p2.x ** 2 + p2.y ** 2 - directrix_y ** 2)
        
        a = a1 - a2
        b = b1 - b2
        c = c1 - c2
        
        discriminant = b ** 2 - 4 * a * c
        
        # Si le discriminant est négatif, pas d'intersection réelle
        if discriminant < -1e-10:  # Marge pour les erreurs d'arrondi
            return (float('nan'), float('nan'))
        elif abs(discriminant) < 1e-10:  # Discriminant presque nul
            sqrt_disc = 0
        else:
            sqrt_disc = math.sqrt(max(0, discriminant))
        
        x1 = (-b - sqrt_disc) / (2 * a)
        x2 = (-b + sqrt_disc) / (2 * a)
        
        # Trier les résultats
        if x1 <= x2:
            return (x1, x2)
        else:
            return (x2, x1)