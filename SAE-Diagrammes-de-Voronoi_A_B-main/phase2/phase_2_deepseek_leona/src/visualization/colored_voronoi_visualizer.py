"""
Module pour la visualisation en couleur du diagramme de Voronoï.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import numpy as np
from typing import List, Dict, Optional, Tuple
from src.models.point import Point


class ColoredVoronoiVisualizer:
    """
    Visualiseur de diagramme de Voronoï avec cellules colorées.
    """
    
    def __init__(self, figure_size: Tuple[int, int] = (12, 10)):
        self.figure_size = figure_size
        self.figure = None
        self.axes = None
        self.cmap = plt.cm.Set3  # Palette de couleurs qualitative
        
    def create_figure(self, title: str = "Diagramme de Voronoï - Cellules colorées") -> None:
        """Crée une nouvelle figure."""
        self.figure, self.axes = plt.subplots(figsize=self.figure_size)
        self.axes.set_title(title, fontsize=16, fontweight='bold')
        self.axes.set_aspect('equal')
        self.axes.grid(True, linestyle='--', alpha=0.3, color='gray')
        
    def plot_colored_cells(self, cells: Dict[Point, List[Point]], 
                          points: List[Point],
                          alpha: float = 0.7,
                          edge_color: str = 'black',
                          edge_width: float = 1.0) -> None:
        """
        Trace les cellules de Voronoï avec des couleurs différentes.
        
        Args:
            cells: Dictionnaire {point_site: liste_des_sommets_de_la_cellule}
            points: Liste des points sites
            alpha: Transparence des cellules
            edge_color: Couleur des bordures
            edge_width: Épaisseur des bordures
        """
        if not self.axes:
            raise RuntimeError("La figure n'a pas été créée. Appelez create_figure() d'abord.")
        
        # Créer une palette de couleurs basée sur le nombre de cellules
        n_cells = len(cells)
        colors = [self.cmap(i % self.cmap.N) for i in range(n_cells)]
        
        patches_list = []
        
        # Pour chaque cellule
        for i, (site, vertices) in enumerate(cells.items()):
            if len(vertices) < 3:
                continue
            
            # Convertir les sommets en liste de tuples (x, y)
            polygon_vertices = [(v.x, v.y) for v in vertices]
            
            # Créer le polygone
            polygon = Polygon(polygon_vertices, 
                            closed=True,
                            facecolor=colors[i],
                            edgecolor=edge_color,
                            linewidth=edge_width,
                            alpha=alpha)
            
            patches_list.append(polygon)
            self.axes.add_patch(polygon)
        
        # Ajouter les points sites
        if points:
            x_coords = [p.x for p in points]
            y_coords = [p.y for p in points]
            
            self.axes.scatter(x_coords, y_coords, 
                            color='red', 
                            s=100, 
                            zorder=10,
                            edgecolor='white',
                            linewidth=2,
                            label='Sites')
    
    def plot_edges_only(self, edges: List, color: str = 'black', 
                        linewidth: float = 1.0, alpha: float = 1.0) -> None:
        """Trace uniquement les arêtes (optionnel)."""
        if not self.axes:
            raise RuntimeError("La figure n'a pas été créée.")
        
        for edge in edges:
            if hasattr(edge, 'start') and hasattr(edge, 'end') and edge.start and edge.end:
                self.axes.plot([edge.start.x, edge.end.x],
                              [edge.start.y, edge.end.y],
                              color=color, linewidth=linewidth, alpha=alpha)
    
    def set_axis_limits(self, x_min: float, x_max: float, 
                        y_min: float, y_max: float, padding: float = 5.0) -> None:
        """Définit les limites des axes avec une marge."""
        if not self.axes:
            raise RuntimeError("La figure n'a pas été créée.")
        
        self.axes.set_xlim(x_min - padding, x_max + padding)
        self.axes.set_ylim(y_min - padding, y_max + padding)
    
    def auto_set_limits(self, cells: Dict[Point, List[Point]], 
                        points: List[Point], padding: float = 5.0) -> None:
        """Définit automatiquement les limites à partir des données."""
        all_x = []
        all_y = []
        
        for vertices in cells.values():
            for v in vertices:
                all_x.append(v.x)
                all_y.append(v.y)
        
        for p in points:
            all_x.append(p.x)
            all_y.append(p.y)
        
        if all_x and all_y:
            self.set_axis_limits(min(all_x), max(all_x), 
                                min(all_y), max(all_y), padding)
    
    def add_labels(self, xlabel: str = "X", ylabel: str = "Y") -> None:
        """Ajoute des labels aux axes."""
        if self.axes:
            self.axes.set_xlabel(xlabel, fontsize=12)
            self.axes.set_ylabel(ylabel, fontsize=12)
            self.axes.legend(fontsize=10, loc='upper right')
    
    def show(self) -> None:
        """Affiche la figure."""
        if self.figure:
            plt.tight_layout()
            plt.show()
    
    def save(self, output_path: str, dpi: int = 300) -> None:
        """Sauvegarde la figure."""
        if self.figure:
            self.figure.savefig(output_path, dpi=dpi, bbox_inches='tight', 
                              facecolor='white', edgecolor='none')
    
    def clear(self) -> None:
        """Efface la figure."""
        if self.axes:
            self.axes.clear()
    
    def close(self) -> None:
        """Ferme la figure."""
        if self.figure:
            plt.close(self.figure)
            self.figure = None
            self.axes = None