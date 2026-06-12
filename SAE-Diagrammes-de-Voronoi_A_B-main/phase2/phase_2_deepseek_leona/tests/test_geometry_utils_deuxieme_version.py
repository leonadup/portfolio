"""
Tests unitaires pour le module geometry_utils.
"""

import pytest
import math
from src.models.point import Point
from src.algorithms.geometry_utils import GeometryUtils


class TestGeometryUtils:
    """Tests pour la classe GeometryUtils."""
    
    def setup_method(self):
        """Initialisation avant chaque test."""
        self.utils = GeometryUtils()
    
    def test_calculate_circle_center_three_points(self):
        """Test le calcul du centre du cercle avec trois points."""
        # Points formant un triangle équilatéral
        p1 = Point(0, 0)
        p2 = Point(2, 0)
        p3 = Point(1, math.sqrt(3))
        
        center = self.utils.calculate_circle_center(p1, p2, p3)
        
        assert center is not None
        # Le centre devrait être à (1, √3/3) approximativement
        assert abs(center.x - 1) < 1e-10
        assert abs(center.y - math.sqrt(3)/3) < 1e-10
    
    def test_calculate_circle_center_colinear_points(self):
        """Test avec des points colinéaires."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(2, 2)
        
        center = self.utils.calculate_circle_center(p1, p2, p3)
        
        assert center is None
    
    def test_is_point_in_circle(self):
        """Test la vérification de présence dans un cercle."""
        center = Point(0, 0)
        radius = 5
        
        # Point à l'intérieur
        p_inside = Point(3, 4)  # Distance 5
        assert self.utils.is_point_in_circle(p_inside, center, radius) == True
        
        # Point à l'extérieur
        p_outside = Point(5, 5)  # Distance ≈7.07
        assert self.utils.is_point_in_circle(p_outside, center, radius) == False
        
        # Point sur le cercle (avec tolérance)
        p_on = Point(5, 0)  # Distance exactement 5
        assert self.utils.is_point_in_circle(p_on, center, radius) == True
    
    def test_is_point_in_circle_with_epsilon(self):
        """Test la vérification avec une tolérance personnalisée."""
        center = Point(0, 0)
        radius = 5
        p_on = Point(5, 0)
        
        # Sans tolérance (epsilon par défaut)
        assert self.utils.is_point_in_circle(p_on, center, radius) == True
        
        # Avec une très petite tolérance
        assert self.utils.is_point_in_circle(p_on, center, radius, 1e-10) == True
    
    def test_calculate_parabola_intersection_same_y(self):
        """Test l'intersection de paraboles avec le même y."""
        p1 = Point(0, 5)
        p2 = Point(10, 5)
        directrix_y = 0
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # Avec des foyers de même hauteur, l'intersection devrait être à x=5
        assert abs(x1 - 5) < 1e-10
        assert abs(x2 - 5) < 1e-10
    
    def test_calculate_parabola_intersection_different_y(self):
        """Test l'intersection de paraboles avec des y différents."""
        p1 = Point(0, 10)
        p2 = Point(10, 5)
        directrix_y = 0
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # Les deux points d'intersection devraient exister
        assert not math.isnan(x1)
        assert not math.isnan(x2)
        assert x1 <= x2
        # Vérifier que les valeurs sont des nombres réels
        assert math.isfinite(x1)
        assert math.isfinite(x2)
    
    def test_calculate_parabola_intersection_parallel_case(self):
        """Test le cas où les paraboles sont presque parallèles."""
        p1 = Point(0, 1)
        p2 = Point(0, 1.0001)  # Points très proches
        directrix_y = 0
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # Dans ce cas, les paraboles sont presque parallèles
        # La fonction devrait retourner inf ou des valeurs très grandes
        assert math.isinf(x1) or abs(x1) > 1e6 or math.isinf(x2) or abs(x2) > 1e6
    
    def test_calculate_parabola_intersection_vertical_focus(self):
        """Test avec des foyers alignés verticalement."""
        p1 = Point(5, 10)
        p2 = Point(5, 5)
        directrix_y = 0
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # La médiatrice est verticale, les paraboles s'intersectent en un point
        assert not math.isnan(x1)
        assert not math.isnan(x2)
        assert math.isfinite(x1)
        assert math.isfinite(x2)
        assert abs(x1 - x2) < 1e-10  # Un seul point d'intersection
    
    def test_calculate_parabola_intersection_directrix_too_close(self):
        """Test quand la directrice est trop proche des foyers."""
        p1 = Point(0, 0.1)
        p2 = Point(0, 0.2)
        directrix_y = 0  # Très proche des foyers
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # La fonction devrait retourner inf dans ce cas
        assert math.isinf(x1) or math.isinf(x2)
    
    def test_calculate_parabola_intersection_negative_discriminant(self):
        """Test avec un discriminant négatif (pas d'intersection)."""
        p1 = Point(0, 10)
        p2 = Point(0, 9.999)  # Points très proches
        directrix_y = 100  # Directrice très éloignée
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # Dans certains cas, le discriminant peut être négatif
        # La fonction devrait retourner inf
        assert math.isinf(x1) or math.isinf(x2)