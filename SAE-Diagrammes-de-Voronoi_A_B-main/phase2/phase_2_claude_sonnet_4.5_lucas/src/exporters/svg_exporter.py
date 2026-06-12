"""
Module d'export en format SVG.

Ce module fournit un exporteur pour sauvegarder les diagrammes
de Voronoï au format SVG (Scalable Vector Graphics).
"""

from typing import List
from src.domain.voronoi_diagram import VoronoiDiagram, VoronoiEdge
from src.domain.point import Point
from src.exporters.base_exporter import BaseExporter, ExporterError


class SVGExporter(BaseExporter):
    """
    Exporteur de diagrammes au format SVG.
    
    Cette classe crée des fichiers SVG vectoriels qui peuvent être
    visualisés dans un navigateur ou éditeur d'images.
    """
    
    def __init__(self, width: int = 800, height: int = 600) -> None:
        """
        Initialise l'exporteur SVG.
        
        Args:
            width: Largeur du SVG en pixels (défaut: 800).
            height: Hauteur du SVG en pixels (défaut: 600).
        """
        self._width = width
        self._height = height
        self._margin = 50
    
    def export(self, diagram: VoronoiDiagram, output_path: str) -> None:
        """
        Exporte le diagramme au format SVG.
        
        Args:
            diagram: Le diagramme à exporter.
            output_path: Chemin vers le fichier de sortie.
            
        Raises:
            ExporterError: Si l'export échoue.
        """
        try:
            svg_content = self._generate_svg(diagram)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
                
        except IOError as e:
            raise ExporterError(f"Erreur lors de l'écriture du fichier : {e}")
    
    def get_file_extension(self) -> str:
        """Retourne l'extension de fichier SVG."""
        return '.svg'
    
    def _generate_svg(self, diagram: VoronoiDiagram) -> str:
        """
        Génère le contenu SVG du diagramme.
        
        Args:
            diagram: Le diagramme à convertir en SVG.
            
        Returns:
            Le contenu SVG complet.
        """
        min_x, min_y, max_x, max_y = diagram.bounding_box
        
        # Calcul de la transformation pour adapter au canvas
        scale_x = (self._width - 2 * self._margin) / (max_x - min_x) if max_x != min_x else 1
        scale_y = (self._height - 2 * self._margin) / (max_y - min_y) if max_y != min_y else 1
        scale = min(scale_x, scale_y)
        
        # Début du SVG
        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self._width}" height="{self._height}" '
            'xmlns="http://www.w3.org/2000/svg">',
            f'  <title>Diagramme de Voronoï - {len(diagram.sites)} sites</title>',
            '  <desc>Généré par Voronoi Diagram Application</desc>',
            '',
            '  <!-- Fond blanc -->',
            f'  <rect width="{self._width}" height="{self._height}" fill="white"/>',
            ''
        ]
        
        # Groupe pour les arêtes
        svg_lines.append('  <!-- Arêtes du diagramme -->')
        svg_lines.append('  <g id="edges" stroke="#2563eb" stroke-width="1.5" fill="none">')
        
        for edge in diagram.edges:
            x1, y1 = self._transform_point(edge.start, min_x, min_y, scale)
            x2, y2 = self._transform_point(edge.end, min_x, min_y, scale)
            svg_lines.append(f'    <line x1="{x1:.2f}" y1="{y1:.2f}" '
                           f'x2="{x2:.2f}" y2="{y2:.2f}"/>')
        
        svg_lines.append('  </g>')
        svg_lines.append('')
        
        # Groupe pour les sommets
        svg_lines.append('  <!-- Sommets du diagramme -->')
        svg_lines.append('  <g id="vertices" fill="#dc2626">')
        
        for vertex in diagram.vertices:
            x, y = self._transform_point(vertex, min_x, min_y, scale)
            svg_lines.append(f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="2"/>')
        
        svg_lines.append('  </g>')
        svg_lines.append('')
        
        # Groupe pour les sites (points générateurs)
        svg_lines.append('  <!-- Sites générateurs -->')
        svg_lines.append('  <g id="sites" fill="#16a34a">')
        
        for site in diagram.sites:
            x, y = self._transform_point(site, min_x, min_y, scale)
            svg_lines.append(f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="4"/>')
        
        svg_lines.append('  </g>')
        svg_lines.append('')
        
        # Légende
        svg_lines.extend([
            '  <!-- Légende -->',
            '  <g id="legend" font-family="Arial, sans-serif" font-size="12">',
            '    <rect x="10" y="10" width="200" height="80" '
            'fill="white" stroke="black" opacity="0.9"/>',
            '    <circle cx="25" cy="30" r="4" fill="#16a34a"/>',
            '    <text x="35" y="35">Sites générateurs</text>',
            '    <circle cx="25" cy="50" r="2" fill="#dc2626"/>',
            '    <text x="35" y="55">Sommets de Voronoï</text>',
            '    <line x1="15" y1="70" x2="35" y2="70" '
            'stroke="#2563eb" stroke-width="1.5"/>',
            '    <text x="40" y="75">Arêtes de Voronoï</text>',
            '  </g>',
            '',
            '</svg>'
        ])
        
        return '\n'.join(svg_lines)
    
    def _transform_point(self, point: Point, min_x: float, min_y: float, 
                        scale: float) -> tuple:
        """
        Transforme un point du diagramme en coordonnées SVG.
        
        Args:
            point: Le point à transformer.
            min_x: Coordonnée x minimale du diagramme.
            min_y: Coordonnée y minimale du diagramme.
            scale: Facteur d'échelle.
            
        Returns:
            Tuple (x, y) des coordonnées transformées.
        """
        # Transformer et centrer
        x = self._margin + (point.x - min_x) * scale
        # Inverser Y car SVG a l'origine en haut à gauche
        y = self._height - (self._margin + (point.y - min_y) * scale)
        
        return (x, y)