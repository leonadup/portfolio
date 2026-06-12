"""
Tests unitaires pour les utilitaires géométriques.

Ces tests vérifient les calculs géométriques selon les principes du TDD.
"""

import pytest
import math
from src.domain.point import Point
from src.algorithms.geometry_utils import (
    calculate_circumcenter,
    calculate_perpendicular_bisector,
    line_intersection,
    point_on_segment,
    clip_line_to_bbox,
    are_collinear
)


class TestCircumcenter:
    """Tests du calcul du centre du cercle circonscrit."""
    
    def test_circumcenter_right_triangle(self):
        """Test : Centre du cercle circonscrit d'un triangle rectangle."""
        p1 = Point(0, 0)
        p2 = Point(4, 0)
        p3 = Point(0, 3)
        
        center = calculate_circumcenter(p1, p2, p3)
        
        assert center is not None
        assert abs(center.x - 2.0) < 1e-9
        assert abs(center.y - 1.5) < 1e-9
    
    def test_circumcenter_equilateral_triangle(self):
        """Test : Centre d'un triangle équilatéral."""
        p1 = Point(0, 0)
        p2 = Point(2, 0)
        p3 = Point(1, math.sqrt(3))
        
        center = calculate_circumcenter(p1, p2, p3)
        
        assert center is not None
        # Le centre devrait être à (1, sqrt(3)/3)
        assert abs(center.x - 1.0) < 1e-9
    
    def test_circumcenter_collinear_points_returns_none(self):
        """Test : Points colinéaires retournent None."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(2, 2)
        
        center = calculate_circumcenter(p1, p2, p3)
        
        assert center is None


class TestPerpendicularBisector:
    """Tests du calcul de la médiatrice."""
    
    def test_perpendicular_bisector_horizontal_segment(self):
        """Test : Médiatrice d'un segment horizontal."""
        p1 = Point(0, 0)
        p2 = Point(4, 0)
        
        a, b, c = calculate_perpendicular_bisector(p1, p2)
        
        # La médiatrice devrait être verticale : x = 2
        # Sous forme ax + by + c = 0 : 1*x + 0*y - 2 = 0
        assert abs(b) < 1e-9  # b devrait être ~0 (ligne verticale)
        
        # Vérifier que le point milieu est sur la ligne
        mid_point = Point(2, 0)
        assert abs(a * mid_point.x + b * mid_point.y + c) < 1e-9
    
    def test_perpendicular_bisector_vertical_segment(self):
        """Test : Médiatrice d'un segment vertical."""
        p1 = Point(0, 0)
        p2 = Point(0, 4)
        
        a, b, c = calculate_perpendicular_bisector(p1, p2)
        
        # La médiatrice devrait être horizontale : y = 2
        assert abs(a) < 1e-9  # a devrait être ~0 (ligne horizontale)
    
    def test_perpendicular_bisector_identical_points_raises_error(self):
        """Test : Médiatrice de deux points identiques lève une erreur."""
        p1 = Point(5, 10)
        p2 = Point(5, 10)
        
        with pytest.raises(ValueError):
            calculate_perpendicular_bisector(p1, p2)


class TestLineIntersection:
    """Tests du calcul d'intersection de droites."""
    
    def test_line_intersection_perpendicular_lines(self):
        """Test : Intersection de deux droites perpendiculaires."""
        # Ligne 1 : y = 0 (axe x)
        # Ligne 2 : x = 0 (axe y)
        intersection = line_intersection(0, 1, 0,  # y = 0
                                        1, 0, 0)   # x = 0
        
        assert intersection is not None
        assert intersection == Point(0, 0)
    
    def test_line_intersection_diagonal_lines(self):
        """Test : Intersection de deux droites diagonales."""
        # Ligne 1 : y = x
        # Ligne 2 : y = -x + 4
        # ax + by + c = 0
        # y - x = 0  ->  -x + y + 0 = 0
        # y + x - 4 = 0  ->  x + y - 4 = 0
        intersection = line_intersection(-1, 1, 0,
                                        1, 1, -4)
        
        assert intersection is not None
        assert abs(intersection.x - 2.0) < 1e-9
        assert abs(intersection.y - 2.0) < 1e-9
    
    def test_line_intersection_parallel_lines_returns_none(self):
        """Test : Droites parallèles retournent None."""
        # Deux lignes horizontales : y = 0 et y = 1
        intersection = line_intersection(0, 1, 0,
                                        0, 1, -1)
        
        assert intersection is None


class TestPointOnSegment:
    """Tests de vérification qu'un point est sur un segment."""
    
    def test_point_on_segment_middle(self):
        """Test : Point au milieu d'un segment."""
        seg_start = Point(0, 0)
        seg_end = Point(4, 0)
        point = Point(2, 0)
        
        assert point_on_segment(point, seg_start, seg_end) is True
    
    def test_point_on_segment_endpoint(self):
        """Test : Point à l'extrémité d'un segment."""
        seg_start = Point(0, 0)
        seg_end = Point(4, 0)
        
        assert point_on_segment(seg_start, seg_start, seg_end) is True
        assert point_on_segment(seg_end, seg_start, seg_end) is True
    
    def test_point_not_on_segment(self):
        """Test : Point pas sur le segment."""
        seg_start = Point(0, 0)
        seg_end = Point(4, 0)
        point = Point(2, 1)  # Au-dessus du segment
        
        assert point_on_segment(point, seg_start, seg_end) is False
    
    def test_point_on_line_but_outside_segment(self):
        """Test : Point sur la ligne mais en dehors du segment."""
        seg_start = Point(0, 0)
        seg_end = Point(2, 0)
        point = Point(4, 0)  # Sur la ligne mais après seg_end
        
        assert point_on_segment(point, seg_start, seg_end) is False


class TestClipLineToBbox:
    """Tests du clipping de lignes."""
    
    def test_clip_line_entirely_inside(self):
        """Test : Ligne entièrement à l'intérieur."""
        p1 = Point(1, 1)
        p2 = Point(3, 3)
        
        result = clip_line_to_bbox(p1, p2, 0, 0, 5, 5)
        
        assert result is not None
        clipped_start, clipped_end = result
        assert clipped_start == p1
        assert clipped_end == p2
    
    def test_clip_line_entirely_outside(self):
        """Test : Ligne entièrement à l'extérieur."""
        p1 = Point(-2, -2)
        p2 = Point(-1, -1)
        
        result = clip_line_to_bbox(p1, p2, 0, 0, 5, 5)
        
        assert result is None
    
    def test_clip_line_partially_inside(self):
        """Test : Ligne partiellement à l'intérieur."""
        p1 = Point(-1, 2)
        p2 = Point(3, 2)
        
        result = clip_line_to_bbox(p1, p2, 0, 0, 5, 5)
        
        assert result is not None
        clipped_start, clipped_end = result
        
        # Le point de début devrait être clippé à x=0
        assert abs(clipped_start.x - 0) < 1e-9
        assert abs(clipped_start.y - 2) < 1e-9
        
        # Le point de fin devrait rester inchangé
        assert clipped_end == p2


class TestCollinear:
    """Tests de vérification de colinéarité."""
    
    def test_collinear_points_on_line(self):
        """Test : Points sur une même ligne."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(2, 2)
        
        assert are_collinear(p1, p2, p3) is True
    
    def test_non_collinear_points(self):
        """Test : Points non colinéaires."""
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(0, 1)
        
        assert are_collinear(p1, p2, p3) is False
    
    def test_collinear_horizontal_line(self):
        """Test : Points sur une ligne horizontale."""
        p1 = Point(0, 5)
        p2 = Point(3, 5)
        p3 = Point(7, 5)
        
        assert are_collinear(p1, p2, p3) is True
    
    def test_collinear_vertical_line(self):
        """Test : Points sur une ligne verticale."""
        p1 = Point(5, 0)
        p2 = Point(5, 3)
        p3 = Point(5, 7)
        
        assert are_collinear(p1, p2, p3) is True