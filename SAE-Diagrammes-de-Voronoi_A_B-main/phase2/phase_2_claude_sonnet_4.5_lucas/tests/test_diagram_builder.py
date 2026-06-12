"""
Tests unitaires pour le service DiagramBuilder.

Ces tests vérifient la construction de diagrammes selon les principes du TDD.
"""

import pytest
from src.domain.point import Point
from src.services.diagram_builder import DiagramBuilder, DiagramBuilderError


class TestDiagramBuilderValidInput:
    """Tests avec des entrées valides."""
    
    def test_build_diagram_with_two_points(self):
        """Test : Construire un diagramme avec 2 points."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0)]
        
        diagram = builder.build_diagram(points)
        
        assert diagram is not None
        assert len(diagram.sites) == 2
        assert len(diagram.edges) > 0
    
    def test_build_diagram_with_three_points(self):
        """Test : Construire un diagramme avec 3 points."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(4, 0), Point(2, 3)]
        
        diagram = builder.build_diagram(points)
        
        assert diagram is not None
        assert len(diagram.sites) == 3
        assert len(diagram.edges) > 0
        assert len(diagram.vertices) > 0
    
    def test_build_diagram_with_multiple_points(self):
        """Test : Construire un diagramme avec plusieurs points."""
        builder = DiagramBuilder()
        points = [
            Point(0, 0),
            Point(10, 0),
            Point(10, 10),
            Point(0, 10),
            Point(5, 5)
        ]
        
        diagram = builder.build_diagram(points)
        
        assert diagram is not None
        assert len(diagram.sites) == 5
        assert len(diagram.edges) > 0
    
    def test_build_diagram_removes_duplicates(self):
        """Test : Les doublons sont supprimés."""
        builder = DiagramBuilder()
        points = [
            Point(0, 0),
            Point(10, 0),
            Point(0, 0),  # Doublon
            Point(10, 0)  # Doublon
        ]
        
        diagram = builder.build_diagram(points)
        
        assert len(diagram.sites) == 2  # Seulement 2 points uniques


class TestDiagramBuilderInvalidInput:
    """Tests avec des entrées invalides."""
    
    def test_build_diagram_with_empty_list_raises_error(self):
        """Test : Liste vide lève une erreur."""
        builder = DiagramBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_diagram([])
        
        assert "vide" in str(exc_info.value)
    
    def test_build_diagram_with_single_point_raises_error(self):
        """Test : Un seul point lève une erreur."""
        builder = DiagramBuilder()
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_diagram([Point(0, 0)])
        
        assert "Au moins 2" in str(exc_info.value)
    
    def test_build_diagram_with_only_duplicates_raises_error(self):
        """Test : Seulement des doublons lève une erreur."""
        builder = DiagramBuilder()
        points = [Point(5, 5), Point(5, 5), Point(5, 5)]
        
        with pytest.raises(ValueError) as exc_info:
            builder.build_diagram(points)
        
        assert "distincts" in str(exc_info.value)


class TestDiagramBuilderValidation:
    """Tests de validation."""
    
    def test_validate_valid_points(self):
        """Test : Valider des points valides."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0)]
        
        assert builder.validate_points(points) is True
    
    def test_validate_empty_list(self):
        """Test : Valider une liste vide."""
        builder = DiagramBuilder()
        
        assert builder.validate_points([]) is False
    
    def test_validate_single_point(self):
        """Test : Valider un seul point."""
        builder = DiagramBuilder()
        
        assert builder.validate_points([Point(0, 0)]) is False
    
    def test_validate_duplicates_only(self):
        """Test : Valider seulement des doublons."""
        builder = DiagramBuilder()
        points = [Point(5, 5), Point(5, 5)]
        
        assert builder.validate_points(points) is False


class TestDiagramBuilderStatistics:
    """Tests des statistiques de diagramme."""
    
    def test_get_statistics(self):
        """Test : Obtenir les statistiques d'un diagramme."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        
        diagram = builder.build_diagram(points)
        stats = builder.get_statistics(diagram)
        
        assert 'num_sites' in stats
        assert 'num_edges' in stats
        assert 'num_vertices' in stats
        assert 'bounding_box' in stats
        assert 'avg_edges_per_site' in stats
        
        assert stats['num_sites'] == 3
        assert stats['num_edges'] > 0
        assert stats['avg_edges_per_site'] > 0