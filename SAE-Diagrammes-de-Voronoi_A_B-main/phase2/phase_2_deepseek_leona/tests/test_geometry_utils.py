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
    
    def test_calculate_parabola_intersection_no_intersection(self):
        """Test le cas où les paraboles ne s'intersectent pas."""
        p1 = Point(0, 1)
        p2 = Point(0, 2)
        directrix_y = 0
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # Avec des paramètres très proches, l'intersection peut être infinie
        assert math.isinf(x1) or math.isnan(x1)
    
    def test_calculate_parabola_intersection_vertical(self):
        """Test avec des foyers alignés verticalement."""
        p1 = Point(5, 10)
        p2 = Point(5, 5)
        directrix_y = 0
        
        x1, x2 = self.utils.calculate_parabola_intersection(p1, p2, directrix_y)
        
        # La médiatrice est verticale, les paraboles s'intersectent en un point
        assert not math.isnan(x1)
        assert not math.isnan(x2)