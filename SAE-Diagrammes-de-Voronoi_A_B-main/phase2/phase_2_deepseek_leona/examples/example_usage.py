#!/usr/bin/env python3
"""
Exemple d'utilisation de l'application de diagramme de Voronoï.
"""

import os
import sys

# Ajout du chemin parent pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.point import Point
from src.algorithms.fortune_algorithm import FortuneAlgorithm
from src.visualization.voronoi_visualizer import VoronoiVisualizer
from src.io.exporters.svg_exporter import SVGExporter


def create_sample_points():
    """Crée un ensemble de points d'exemple."""
    return [
        Point(10, 10),
        Point(20, 15),
        Point(30, 10),
        Point(15, 25),
        Point(25, 30),
        Point(35, 25),
        Point(20, 40),
        Point(30, 45),
    ]


def main():
    """Fonction principale d'exemple."""
    print("Génération d'un diagramme de Voronoï d'exemple...")
    
    # Création des points
    points = create_sample_points()
    print(f"Nombre de points: {len(points)}")
    
    # Génération du diagramme
    generator = FortuneAlgorithm()
    edges = generator.generate(points)
    print(f"Nombre d'arêtes générées: {len(edges)}")
    
    # Visualisation
    print("Création de la visualisation...")
    visualizer = VoronoiVisualizer()
    visualizer.create_figure("Diagramme de Voronoï - Exemple")
    visualizer.plot_edges(edges, color='blue', linewidth=1.5)
    visualizer.plot_points(points, color='red', markersize=8)
    visualizer.auto_set_limits(edges, points, padding=5)
    visualizer.add_labels("X", "Y")
    
    # Sauvegarde
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    svg_path = os.path.join(output_dir, "voronoi_example.svg")
    visualizer.save(svg_path)
    print(f"✓ Diagramme sauvegardé: {svg_path}")
    
    # Export SVG séparé
    svg_exporter = SVGExporter(width=800, height=600)
    svg_exporter.export(edges, points, os.path.join(output_dir, "voronoi_export.svg"))
    print(f"✓ Export SVG: {os.path.join(output_dir, 'voronoi_export.svg')}")
    
    # Affichage
    print("Affichage du diagramme...")
    visualizer.show()
    
    print("Exemple terminé!")


if __name__ == "__main__":
    main()