"""
Module pour la visualisation interactive du diagramme de Voronoï.
"""

import matplotlib.pyplot as plt
from typing import List, Optional, Tuple
from src.models.point import Point
from src.models.edge import Edge


class VoronoiVisualizer:
    """
    Responsable de la visualisation du diagramme de Voronoï.
    
    Cette classe utilise matplotlib pour afficher le diagramme de manière interactive.
    """
    
    def __init__(self, figure_size: Tuple[int, int] = (10, 8)):
        """
        Initialise le visualiseur.
        
        Args:
            figure_size: Taille de la figure (largeur, hauteur) en pouces
        """
        self.figure_size = figure_size
        self.figure = None
        self.axes = None
    
    def create_figure(self, title: str = "Diagramme de Voronoï") -> None:
        """
        Crée une nouvelle figure pour la visualisation.
        
        Args:
            title: Titre de la figure
        """
        self.figure, self.axes = plt.subplots(figsize=self.figure_size)
        self.axes.set_title(title)
        self.axes.set_aspect('equal')
        self.axes.grid(True, linestyle='--', alpha=0.7)
    
    def plot_edges(self, edges: List[Edge], color: str = 'black', 
                   linewidth: float = 1.0, alpha: float = 0.8) -> None:
        """
        Trace les arêtes du diagramme.
        
        Args:
            edges: Liste des arêtes à tracer
            color: Couleur des arêtes
            linewidth: Épaisseur des lignes
            alpha: Transparence (0 à 1)
        """
        if not self.axes:
            raise RuntimeError("La figure n'a pas été créée. Appelez create_figure() d'abord.")
        
        for edge in edges:
            if edge.start and edge.end:
                self.axes.plot(
                    [edge.start.x, edge.end.x],
                    [edge.start.y, edge.end.y],
                    color=color,
                    linewidth=linewidth,
                    alpha=alpha
                )
    
    def plot_points(self, points: List[Point], color: str = 'red', 
                    marker: str = 'o', markersize: int = 6) -> None:
        """
        Trace les points source.
        
        Args:
            points: Liste des points à tracer
            color: Couleur des points
            marker: Marqueur matplotlib
            markersize: Taille des marqueurs
        """
        if not self.axes:
            raise RuntimeError("La figure n'a pas été créée. Appelez create_figure() d'abord.")
        
        if points:
            x_coords = [p.x for p in points]
            y_coords = [p.y for p in points]
            
            self.axes.scatter(
                x_coords, y_coords,
                color=color,
                marker=marker,
                s=markersize ** 2,
                zorder=5
            )
    
    def set_axis_limits(self, x_min: float, x_max: float, 
                        y_min: float, y_max: float, padding: float = 1.0) -> None:
        """
        Définit les limites des axes.
        
        Args:
            x_min, x_max: Limites en x
            y_min, y_max: Limites en y
            padding: Marge à ajouter autour
        """
        if not self.axes:
            raise RuntimeError("La figure n'a pas été créée. Appelez create_figure() d'abord.")
        
        self.axes.set_xlim(x_min - padding, x_max + padding)
        self.axes.set_ylim(y_min - padding, y_max + padding)
    
    def auto_set_limits(self, edges: List[Edge], points: List[Point], 
                        padding: float = 1.0) -> None:
        """
        Définit automatiquement les limites à partir des données.
        
        Args:
            edges: Liste des arêtes
            points: Liste des points
            padding: Marge à ajouter autour
        """
        all_x = []
        all_y = []
        
        for edge in edges:
            if edge.start:
                all_x.append(edge.start.x)
                all_y.append(edge.start.y)
            if edge.end:
                all_x.append(edge.end.x)
                all_y.append(edge.end.y)
        
        for point in points:
            all_x.append(point.x)
            all_y.append(point.y)
        
        if all_x and all_y:
            self.set_axis_limits(
                min(all_x), max(all_x),
                min(all_y), max(all_y),
                padding
            )
    
    def add_labels(self, xlabel: str = "X", ylabel: str = "Y") -> None:
        """Ajoute des labels aux axes."""
        if self.axes:
            self.axes.set_xlabel(xlabel)
            self.axes.set_ylabel(ylabel)
    
    def show(self) -> None:
        """Affiche la figure."""
        if self.figure:
            plt.tight_layout()
            plt.show()
    
    def save(self, output_path: str, dpi: int = 300) -> None:
        """
        Sauvegarde la figure dans un fichier.
        
        Args:
            output_path: Chemin du fichier de sortie
            dpi: Résolution en points par pouce
        """
        if self.figure:
            self.figure.savefig(output_path, dpi=dpi, bbox_inches='tight')
    
    def clear(self) -> None:
        """Efface la figure courante."""
        if self.axes:
            self.axes.clear()
    
    def close(self) -> None:
        """Ferme la figure."""
        if self.figure:
            plt.close(self.figure)
            self.figure = None
            self.axes = None