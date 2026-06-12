"""
Module d'export en format image (PNG).

Ce module fournit un exporteur pour sauvegarder les diagrammes
de Voronoï au format PNG en utilisant matplotlib.
"""

import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour Windows
import matplotlib.pyplot as plt
from src.domain.voronoi_diagram import VoronoiDiagram
from src.exporters.base_exporter import BaseExporter, ExporterError


class ImageExporter(BaseExporter):
    """
    Exporteur de diagrammes au format image (PNG).
    
    Cette classe utilise matplotlib pour générer des images raster
    du diagramme de Voronoï.
    """
    
    def __init__(self, width: int = 10, height: int = 8, dpi: int = 100) -> None:
        """
        Initialise l'exporteur d'images.
        
        Args:
            width: Largeur de la figure en pouces (défaut: 10).
            height: Hauteur de la figure en pouces (défaut: 8).
            dpi: Résolution en points par pouce (défaut: 100).
        """
        self._width = width
        self._height = height
        self._dpi = dpi
    
    def export(self, diagram: VoronoiDiagram, output_path: str) -> None:
        """
        Exporte le diagramme au format PNG.
        
        Args:
            diagram: Le diagramme à exporter.
            output_path: Chemin vers le fichier de sortie.
            
        Raises:
            ExporterError: Si l'export échoue.
        """
        try:
            # Créer la figure
            fig, ax = plt.subplots(figsize=(self._width, self._height), dpi=self._dpi)
            
            # Dessiner le diagramme
            self._draw_diagram(ax, diagram)
            
            # Configurer l'apparence
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3)
            ax.set_title(f'Diagramme de Voronoï - {len(diagram.sites)} sites',
                        fontsize=14, fontweight='bold')
            
            # Sauvegarder
            plt.tight_layout()
            plt.savefig(output_path, dpi=self._dpi, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close(fig)
            
        except Exception as e:
            raise ExporterError(f"Erreur lors de l'export PNG : {e}")
    
    def get_file_extension(self) -> str:
        """Retourne l'extension de fichier PNG."""
        return '.png'
    
    def _draw_diagram(self, ax, diagram: VoronoiDiagram) -> None:
        """
        Dessine le diagramme sur un axe matplotlib.
        
        Args:
            ax: L'axe matplotlib sur lequel dessiner.
            diagram: Le diagramme à dessiner.
        """
        # Dessiner les arêtes
        for edge in diagram.edges:
            x_coords = [edge.start.x, edge.end.x]
            y_coords = [edge.start.y, edge.end.y]
            ax.plot(x_coords, y_coords, 'b-', linewidth=1.5, 
                   label='Arêtes' if edge == diagram.edges[0] else '')
        
        # Dessiner les sommets
        if diagram.vertices:
            vertices_x = [v.x for v in diagram.vertices]
            vertices_y = [v.y for v in diagram.vertices]
            ax.plot(vertices_x, vertices_y, 'ro', markersize=4, 
                   label='Sommets', zorder=5)
        
        # Dessiner les sites générateurs
        sites_x = [s.x for s in diagram.sites]
        sites_y = [s.y for s in diagram.sites]
        ax.plot(sites_x, sites_y, 'go', markersize=8, 
               label='Sites', zorder=10, markeredgecolor='darkgreen',
               markeredgewidth=1.5)
        
        # Configurer les limites
        min_x, min_y, max_x, max_y = diagram.bounding_box
        margin = 0.05 * max(max_x - min_x, max_y - min_y)
        ax.set_xlim(min_x - margin, max_x + margin)
        ax.set_ylim(min_y - margin, max_y + margin)
        
        # Ajouter la légende
        ax.legend(loc='upper right', framealpha=0.9)
        
        # Labels des axes
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)