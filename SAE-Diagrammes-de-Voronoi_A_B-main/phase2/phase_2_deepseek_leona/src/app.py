"""
Application principale pour la génération et visualisation de diagrammes de Voronoï.
"""

import os
import sys
from typing import Optional, List
import argparse

# Ajout du chemin parent pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.point import Point
from src.models.edge import Edge
from src.io.point_reader import PointReader
from src.algorithms.fortune_algorithm import FortuneAlgorithm
from src.algorithms.voronoi_cell_generator import VoronoiCellGenerator
from src.visualization.colored_voronoi_visualizer import ColoredVoronoiVisualizer
from src.io.exporters.svg_exporter import SVGExporter
from src.performance.benchmark import Benchmark


class VoronoiApplication:
    """
    Classe principale de l'application.
    """
    
    def __init__(self):
        """Initialise l'application avec ses composants."""
        self.generator = FortuneAlgorithm()
        self.cell_generator = VoronoiCellGenerator()
        self.visualizer = ColoredVoronoiVisualizer()
        self.svg_exporter = SVGExporter()
        self.current_points: List[Point] = []
        self.current_edges: List[Edge] = []
        self.current_cells = {}
        self.benchmark = Benchmark(self.generator)
    
    def load_points_from_file(self, file_path: str) -> List[Point]:
        """
        Charge les points depuis un fichier.
        """
        if not PointReader.validate_file_extension(file_path):
            raise ValueError(f"Extension de fichier non supportée. Utilisez .txt")
        
        reader = PointReader(file_path)
        points = reader.read_points()
        
        self.current_points = points
        print(f"✓ {len(points)} points chargés depuis {file_path}")
        
        return points
    
    def generate_diagram(self) -> dict:
        """
        Génère le diagramme de Voronoï avec cellules colorées.
        """
        if not self.current_points:
            raise ValueError("Aucun point chargé. Chargez d'abord un fichier.")
        
        print(f"Génération du diagramme pour {len(self.current_points)} points...")
        
        # Générer les cellules
        self.current_cells = self.cell_generator.generate(self.current_points)
        
        # Générer aussi les arêtes pour compatibilité
        self.current_edges = self.generator.generate(self.current_points)
        
        print(f"✓ Diagramme généré avec {len(self.current_cells)} cellules")
        
        return self.current_cells
    
    def visualize(self, title: str = "Diagramme de Voronoï - Cellules colorées") -> None:
        """
        Visualise le diagramme avec cellules colorées.
        """
        if not self.current_cells:
            raise ValueError("Aucun diagramme généré. Générez d'abord le diagramme.")
        
        self.visualizer.create_figure(title)
        
        # Tracer les cellules colorées
        self.visualizer.plot_colored_cells(self.current_cells, self.current_points)
        
        # Optionnel : tracer aussi les arêtes pour plus de netteté
        # self.visualizer.plot_edges_only(self.current_edges, color='black', linewidth=1.0)
        
        self.visualizer.auto_set_limits(self.current_cells, self.current_points)
        self.visualizer.add_labels()
        self.visualizer.show()
    
    def export_svg(self, output_path: str) -> None:
        """
        Exporte le diagramme au format SVG.
        """
        if not self.current_edges:
            raise ValueError("Aucun diagramme généré. Générez d'abord le diagramme.")
        
        self.svg_exporter.export(self.current_edges, self.current_points, output_path)
        print(f"✓ Diagramme exporté vers {output_path}")
    
    def export_colored_svg(self, output_path: str) -> None:
        """
        Exporte le diagramme coloré en SVG via matplotlib.
        """
        if not self.current_cells:
            raise ValueError("Aucun diagramme généré. Générez d'abord le diagramme.")
        
        self.visualizer.create_figure("Diagramme de Voronoï - Export")
        self.visualizer.plot_colored_cells(self.current_cells, self.current_points)
        self.visualizer.auto_set_limits(self.current_cells, self.current_points)
        self.visualizer.save(output_path)
        self.visualizer.close()
        print(f"✓ Diagramme coloré exporté vers {output_path}")
    
    def run_benchmark(self, max_points: int = 500, steps: int = 10) -> None:
        """
        Exécute un benchmark de performance.
        """
        point_counts = [int(i * max_points / steps) for i in range(2, steps + 1)]
        
        print(f"Exécution du benchmark avec des échantillons jusqu'à {max_points} points...")
        results = self.benchmark.run_benchmark(point_counts)
        
        print("\nRésultats du benchmark:")
        for n, time_taken in results.items():
            print(f"  {n} points: {time_taken:.6f} secondes")
        
        # Afficher le graphique
        self.benchmark.plot_results()
        
        # Sauvegarder les résultats
        os.makedirs("data/benchmarks", exist_ok=True)
        self.benchmark.export_results("data/benchmarks/results.csv")
        print("✓ Résultats sauvegardés dans data/benchmarks/results.csv")
    
    def interactive_mode(self) -> None:
        """Mode interactif de l'application."""
        print("\n" + "="*60)
        print("Application de Diagramme de Voronoï - Version Cellules Colorées")
        print("="*60)
        
        while True:
            print("\nMenu principal:")
            print("1. Charger un fichier de points")
            print("2. Générer le diagramme (cellules colorées)")
            print("3. Visualiser le diagramme")
            print("4. Exporter en SVG (arêtes seulement)")
            print("5. Exporter en image colorée (PNG/SVG)")
            print("6. Exécuter un benchmark")
            print("7. Quitter")
            
            choice = input("\nVotre choix (1-7): ").strip()
            
            try:
                if choice == '1':
                    file_path = input("Chemin du fichier: ").strip()
                    self.load_points_from_file(file_path)
                
                elif choice == '2':
                    self.generate_diagram()
                
                elif choice == '3':
                    self.visualize()
                
                elif choice == '4':
                    if not self.current_edges:
                        print("Veuillez d'abord générer un diagramme.")
                        continue
                    
                    output = input("Nom du fichier SVG (ex: diagramme.svg): ").strip()
                    if not output.endswith('.svg'):
                        output += '.svg'
                    self.export_svg(output)
                
                elif choice == '5':
                    if not self.current_cells:
                        print("Veuillez d'abord générer un diagramme.")
                        continue
                    
                    output = input("Nom du fichier image (ex: diagramme.png): ").strip()
                    self.export_colored_svg(output)
                
                elif choice == '6':
                    max_points = int(input("Nombre maximum de points (défaut: 500): ") or "500")
                    steps = int(input("Nombre de mesures (défaut: 10): ") or "10")
                    self.run_benchmark(max_points, steps)
                
                elif choice == '7':
                    print("Au revoir!")
                    break
                
                else:
                    print("Choix invalide. Veuillez réessayer.")
                    
            except Exception as e:
                print(f"❌ Erreur: {str(e)}")


def main():
    """Point d'entrée principal de l'application."""
    parser = argparse.ArgumentParser(description="Application de diagramme de Voronoï")
    parser.add_argument("--file", "-f", help="Fichier de points à charger")
    parser.add_argument("--export", "-e", help="Exporter en SVG (spécifier le chemin)")
    parser.add_argument("--export-color", "-c", help="Exporter en image colorée")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Exécuter un benchmark")
    parser.add_argument("--max-points", type=int, default=500, help="Points max pour benchmark")
    
    args = parser.parse_args()
    
    app = VoronoiApplication()
    
    # Mode ligne de commande
    if args.file:
        try:
            app.load_points_from_file(args.file)
            app.generate_diagram()
            
            if args.export:
                app.export_svg(args.export)
            elif args.export_color:
                app.export_colored_svg(args.export_color)
            else:
                app.visualize()
                
        except Exception as e:
            print(f"Erreur: {e}")
            sys.exit(1)
    
    elif args.benchmark:
        app.run_benchmark(args.max_points)
    
    else:
        # Mode interactif
        app.interactive_mode()


if __name__ == "__main__":
    # Import pour le benchmark
    import numpy as np
    main()