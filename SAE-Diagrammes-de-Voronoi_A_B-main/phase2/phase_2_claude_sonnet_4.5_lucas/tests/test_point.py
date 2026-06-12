"""
Tests unitaires pour la classe Point.

Ces tests vérifient le comportement de la classe Point
selon les principes du TDD.
"""

import pytest
import math
from src.domain.point import Point


class TestPointCreation:
    """Tests de création de points."""
    
    def test_create_point_with_integers(self):
        """Test : Créer un point avec des entiers."""
        point = Point(5, 10)
        assert point.x == 5.0
        assert point.y == 10.0
    
    def test_create_point_with_floats(self):
        """Test : Créer un point avec des flottants."""
        point = Point(3.14, 2.71)
        assert point.x == 3.14
        assert point.y == 2.71
    
    def test_create_point_with_negative_values(self):
        """Test : Créer un point avec des valeurs négatives."""
        point = Point(-5.5, -10.2)
        assert point.x == -5.5
        assert point.y == -10.2
    
    def test_create_point_with_zero(self):
        """Test : Créer un point à l'origine."""
        point = Point(0, 0)
        assert point.x == 0.0
        assert point.y == 0.0
    
    def test_create_point_with_invalid_type_raises_error(self):
        """Test : Créer un point avec un type invalide lève une erreur."""
        with pytest.raises(TypeError):
            Point("5", 10)
        
        with pytest.raises(TypeError):
            Point(5, "10")
    
    def test_create_point_with_nan_raises_error(self):
        """Test : Créer un point avec NaN lève une erreur."""
        with pytest.raises(ValueError):
            Point(float('nan'), 5)
        
        with pytest.raises(ValueError):
            Point(5, float('nan'))
    
    def test_create_point_with_infinity_raises_error(self):
        """Test : Créer un point avec l'infini lève une erreur."""
        with pytest.raises(ValueError):
            Point(float('inf'), 5)
        
        with pytest.raises(ValueError):
            Point(5, float('-inf'))


class TestPointDistance:
    """Tests des calculs de distance."""
    
    def test_distance_to_itself_is_zero(self):
        """Test : La distance d'un point à lui-même est 0."""
        point = Point(5, 10)
        assert point.distance_to(point) == 0.0
    
    def test_distance_between_two_points(self):
        """Test : Distance euclidienne entre deux points."""
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        assert p1.distance_to(p2) == 5.0
    
    def test_distance_is_symmetric(self):
        """Test : La distance est symétrique."""
        p1 = Point(1, 2)
        p2 = Point(4, 6)
        assert p1.distance_to(p2) == p2.distance_to(p1)
    
    def test_squared_distance(self):
        """Test : Carré de la distance."""
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        assert p1.squared_distance_to(p2) == 25.0
    
    def test_distance_with_invalid_type_raises_error(self):
        """Test : Calculer la distance avec un type invalide lève une erreur."""
        point = Point(0, 0)
        with pytest.raises(TypeError):
            point.distance_to("not a point")


class TestPointComparison:
    """Tests des comparaisons de points."""
    
    def test_equality_same_coordinates(self):
        """Test : Deux points avec mêmes coordonnées sont égaux."""
        p1 = Point(5, 10)
        p2 = Point(5, 10)
        assert p1 == p2
    
    def test_equality_with_tolerance(self):
        """Test : Égalité avec tolérance numérique."""
        p1 = Point(5.0, 10.0)
        p2 = Point(5.0 + 1e-10, 10.0 + 1e-10)
        assert p1 == p2
    
    def test_inequality_different_x(self):
        """Test : Deux points avec x différents sont inégaux."""
        p1 = Point(5, 10)
        p2 = Point(6, 10)
        assert p1 != p2
    
    def test_inequality_different_y(self):
        """Test : Deux points avec y différents sont inégaux."""
        p1 = Point(5, 10)
        p2 = Point(5, 11)
        assert p1 != p2
    
    def test_equality_with_non_point_returns_false(self):
        """Test : Comparer avec un non-point retourne False."""
        point = Point(5, 10)
        assert point != "not a point"
        assert point != 42
    
    def test_sorting_points(self):
        """Test : Tri des points (par y puis x)."""
        points = [Point(3, 2), Point(1, 1), Point(2, 1)]
        sorted_points = sorted(points)
        assert sorted_points[0] == Point(1, 1)
        assert sorted_points[1] == Point(2, 1)
        assert sorted_points[2] == Point(3, 2)


class TestPointHash:
    """Tests du hachage de points."""
    
    def test_hash_same_for_equal_points(self):
        """Test : Deux points égaux ont le même hash."""
        p1 = Point(5, 10)
        p2 = Point(5, 10)
        assert hash(p1) == hash(p2)
    
    def test_points_can_be_in_set(self):
        """Test : Les points peuvent être dans un set."""
        p1 = Point(5, 10)
        p2 = Point(5, 10)
        p3 = Point(3, 4)
        
        point_set = {p1, p2, p3}
        assert len(point_set) == 2  # p1 et p2 sont identiques


class TestPointConversion:
    """Tests des conversions de points."""
    
    def test_to_tuple(self):
        """Test : Conversion en tuple."""
        point = Point(5.5, 10.2)
        assert point.to_tuple() == (5.5, 10.2)
    
    def test_str_representation(self):
        """Test : Représentation string."""
        point = Point(5.123, 10.456)
        assert str(point) == "(5.12, 10.46)"
    
    def test_repr_representation(self):
        """Test : Représentation repr."""
        point = Point(5, 10)
        assert repr(point) == "Point(5.0, 10.0)"


class TestPointImmutability:
    """Tests de l'immutabilité des points."""
    
    def test_cannot_modify_x(self):
        """Test : Impossible de modifier x."""
        point = Point(5, 10)
        with pytest.raises(AttributeError):
            point.x = 20
    
    def test_cannot_modify_y(self):
        """Test : Impossible de modifier y."""
        point = Point(5, 10)
        with pytest.raises(AttributeError):
            point.y = 20