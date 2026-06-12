"""
Module pour l'exportation en format SVG.
"""

from typing import List, Optional
from src.models.edge import Edge
from src.models.point import Point


class SVGExporter:
    """
    Exporte le diagramme de Voronoï au format SVG.
    
    Cette classe suit le principe de responsabilité unique (SOLID) :
    elle ne s'occupe que de l'exportation SVG.
    """
    
    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialise l'exportateur SVG.
        
        Args:
            width: Largeur de l'image en pixels
            height: Hauteur de l'image en pixels
        """
        self.width = width
        self.height = height
        self.padding = 50
    
    def export(self, edges: List[Edge], points: List[Point], 
               output_path: str, show_points: bool = True) -> None:
        """
        Exporte le diagramme au format SVG.
        
        Args:
            edges: Liste des arêtes à exporter
            points: Liste des points à exporter
            output_path: Chemin du fichier de sortie
            show_points: Afficher les points source
            
        Raises:
            IOError: Si l'écriture du fichier échoue
        """
        # Calcul des limites
        x_min, x_max, y_min, y_max = self._calculate_bounds(edges, points)
        
        # Transformation des coordonnées
        def transform_x(x: float) -> float:
            return self.padding + (x - x_min) * (self.width - 2 * self.padding) / (x_max - x_min)
        
        def transform_y(y: float) -> float:
            return self.padding + (y_max - y) * (self.height - 2 * self.padding) / (y_max - y_min)
        
        # Construction du SVG
        svg_content = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">',
            f'  <rect width="{self.width}" height="{self.height}" fill="white" stroke="none"/>'
        ]
        
        # Ajout des arêtes
        svg_content.append('  <g stroke="black" stroke-width="1">')
        for edge in edges:
            if edge.start and edge.end:
                x1 = transform_x(edge.start.x)
                y1 = transform_y(edge.start.y)
                x2 = transform_x(edge.end.x)
                y2 = transform_y(edge.end.y)
                
                svg_content.append(
                    f'    <line x1="{x1:.2f}" y1="{y1:.2f}" '
                    f'x2="{x2:.2f}" y2="{y2:.2f}" />'
                )
        svg_content.append('  </g>')
        
        # Ajout des points
        if show_points and points:
            svg_content.append('  <g fill="red" stroke="none">')
            for point in points:
                x = transform_x(point.x)
                y = transform_y(point.y)
                svg_content.append(
                    f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="3" />'
                )
            svg_content.append('  </g>')
        
        svg_content.append('</svg>')
        
        # Écriture du fichier
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(svg_content))
        except IOError as e:
            raise IOError(f"Erreur lors de l'écriture du fichier SVG : {str(e)}")
    
    def _calculate_bounds(self, edges: List[Edge], points: List[Point]) -> tuple:
        """
        Calcule les limites du diagramme.
        
        Args:
            edges: Liste des arêtes
            points: Liste des points
            
        Returns:
            tuple: (x_min, x_max, y_min, y_max)
        """
        all_x = []
        all_y = []
        
        # Ajouter les points des arêtes
        for edge in edges:
            if edge.start:
                all_x.append(edge.start.x)
                all_y.append(edge.start.y)
            if edge.end:
                all_x.append(edge.end.x)
                all_y.append(edge.end.y)
        
        # Ajouter les points source
        for point in points:
            all_x.append(point.x)
            all_y.append(point.y)
        
        if not all_x:
            return (0, 1, 0, 1)
        
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        
        # Ajouter une marge
        margin_x = (x_max - x_min) * 0.1 if x_max > x_min else 1
        margin_y = (y_max - y_min) * 0.1 if y_max > y_min else 1
        
        return (x_min - margin_x, x_max + margin_x,
                y_min - margin_y, y_max + margin_y)