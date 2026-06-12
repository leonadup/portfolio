import sys
from pathlib import Path

# Ajoute le chemin du projet à sys.path
sys.path.append(str(Path(__file__).parent))

from parsers.file_parser import FileParser
from services.voronoi_builder import VoronoiBuilder
from services.performance_meter import PerformanceMeter
from visualizers.svg_visualizer import SVGVisualizer

def main():
    file_path = "../example_points.txt"
    output_svg = "voronoi.svg"

    # Parse les points
    points = FileParser.parse(file_path)
    print(f"Nombre de points lus: {len(points)}")

    # Mesure la performance
    time_taken = PerformanceMeter.measure(VoronoiBuilder.build, points)
    print(f"Temps d'exécution: {time_taken:.4f} secondes")

    # Construit le diagramme
    diagram = VoronoiBuilder.build(points)
    print(f"Nombre d'arêtes de Voronoï générées: {len(diagram.get_edges())}")

    # Visualise
    SVGVisualizer.visualize(diagram, output_svg, width=800, height=600)


if __name__ == "__main__":
    main()
