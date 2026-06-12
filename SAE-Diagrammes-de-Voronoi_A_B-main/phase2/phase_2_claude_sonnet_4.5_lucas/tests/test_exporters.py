"""
Tests unitaires pour les exporteurs.

Ces tests vérifient l'export de diagrammes selon les principes du TDD.
"""

import pytest
import os
from src.domain.point import Point
from src.services.diagram_builder import DiagramBuilder
from src.exporters.svg_exporter import SVGExporter
from src.exporters.image_exporter import ImageExporter
from src.exporters.base_exporter import ExporterError


class TestSVGExporter:
    """Tests de l'exporteur SVG."""
    
    def test_export_simple_diagram_to_svg(self, tmp_path):
        """Test : Exporter un diagramme simple en SVG."""
        # Créer un diagramme
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        diagram = builder.build_diagram(points)
        
        # Exporter
        exporter = SVGExporter()
        output_path = tmp_path / "diagram.svg"
        exporter.export(diagram, str(output_path))
        
        # Vérifier que le fichier existe
        assert output_path.exists()
        
        # Vérifier le contenu
        content = output_path.read_text()
        assert '<?xml version="1.0"' in content
        assert '<svg' in content
        assert '</svg>' in content
    
    def test_svg_exporter_file_extension(self):
        """Test : Extension de fichier SVG."""
        exporter = SVGExporter()
        assert exporter.get_file_extension() == '.svg'
    
    def test_svg_exporter_with_custom_dimensions(self, tmp_path):
        """Test : Exporter avec dimensions personnalisées."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0)]
        diagram = builder.build_diagram(points)
        
        exporter = SVGExporter(width=1000, height=800)
        output_path = tmp_path / "diagram.svg"
        exporter.export(diagram, str(output_path))
        
        content = output_path.read_text()
        assert 'width="1000"' in content
        assert 'height="800"' in content
    
    def test_svg_contains_sites(self, tmp_path):
        """Test : Le SVG contient les sites."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        diagram = builder.build_diagram(points)
        
        exporter = SVGExporter()
        output_path = tmp_path / "diagram.svg"
        exporter.export(diagram, str(output_path))
        
        content = output_path.read_text()
        assert 'id="sites"' in content
        assert 'circle' in content
    
    def test_svg_contains_edges(self, tmp_path):
        """Test : Le SVG contient les arêtes."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        diagram = builder.build_diagram(points)
        
        exporter = SVGExporter()
        output_path = tmp_path / "diagram.svg"
        exporter.export(diagram, str(output_path))
        
        content = output_path.read_text()
        assert 'id="edges"' in content
        assert 'line' in content


class TestImageExporter:
    """Tests de l'exporteur d'images."""
    
    def test_export_simple_diagram_to_png(self, tmp_path):
        """Test : Exporter un diagramme simple en PNG."""
        # Créer un diagramme
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        diagram = builder.build_diagram(points)
        
        # Exporter
        exporter = ImageExporter()
        output_path = tmp_path / "diagram.png"
        exporter.export(diagram, str(output_path))
        
        # Vérifier que le fichier existe
        assert output_path.exists()
        
        # Vérifier que c'est bien une image (au moins quelques octets)
        assert output_path.stat().st_size > 1000
    
    def test_image_exporter_file_extension(self):
        """Test : Extension de fichier PNG."""
        exporter = ImageExporter()
        assert exporter.get_file_extension() == '.png'
    
    def test_image_exporter_with_custom_dimensions(self, tmp_path):
        """Test : Exporter avec dimensions personnalisées."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0)]
        diagram = builder.build_diagram(points)
        
        exporter = ImageExporter(width=12, height=9, dpi=150)
        output_path = tmp_path / "diagram.png"
        
        # Ne devrait pas lever d'erreur
        exporter.export(diagram, str(output_path))
        assert output_path.exists()
    
    def test_export_to_invalid_path_raises_error(self, tmp_path):
        """Test : Exporter vers un chemin invalide lève une erreur."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0)]
        diagram = builder.build_diagram(points)
        
        exporter = ImageExporter()
        invalid_path = tmp_path / "nonexistent_dir" / "diagram.png"
        
        with pytest.raises(ExporterError):
            exporter.export(diagram, str(invalid_path))


class TestExporterPolymorphism:
    """Tests du polymorphisme des exporteurs."""
    
    def test_both_exporters_implement_base_interface(self):
        """Test : Les deux exporteurs implémentent l'interface de base."""
        svg_exporter = SVGExporter()
        img_exporter = ImageExporter()
        
        # Les deux doivent avoir les méthodes de base
        assert hasattr(svg_exporter, 'export')
        assert hasattr(svg_exporter, 'get_file_extension')
        assert hasattr(img_exporter, 'export')
        assert hasattr(img_exporter, 'get_file_extension')
    
    def test_exporters_can_be_used_polymorphically(self, tmp_path):
        """Test : Les exporteurs peuvent être utilisés de manière polymorphe."""
        builder = DiagramBuilder()
        points = [Point(0, 0), Point(10, 0), Point(5, 10)]
        diagram = builder.build_diagram(points)
        
        exporters = [SVGExporter(), ImageExporter()]
        
        for i, exporter in enumerate(exporters):
            ext = exporter.get_file_extension()
            output_path = tmp_path / f"diagram_{i}{ext}"
            exporter.export(diagram, str(output_path))
            
            assert output_path.exists()