"""
Point d'entrée principal de l'application Voronoi Diagram.

Ce module fournit une interface en ligne de commande conviviale
pour utiliser toutes les fonctionnalités de l'application.
"""

import os
import sys
from typing import Optional

from src.domain.point import Point
from src.domain.voronoi_diagram import VoronoiDiagram
from src.services.file_reader import FileReader, FileReaderError, InvalidFileFormatError
from src.services.diagram_builder import DiagramBuilder, DiagramBuilderError
from src.services.performance_analyzer import PerformanceAnalyzer
from src.exporters.svg_exporter import SVGExporter
from src.exporters.image_exporter import ImageExporter
from src.exporters.base_exporter import ExporterError
from src.ui.visualizer import Visualizer


class VoronoiApplication:
    """
    Application principale de génération de diagrammes de Voronoï.
    
    Cette classe orchestre toutes les fonctionnalités de l'application
    et fournit une interface utilisateur conviviale.
    """
    
    def __init__(self) -> None:
        """Initialise l'application."""
        self._file_reader = FileReader()
        self._diagram_builder = DiagramBuilder()
        self._visualizer = Visualizer()
        self._current_diagram: Optional[VoronoiDiagram] = None
        self._current_file: Optional[str] = None
        
        # Créer les répertoires de sortie s'ils n'existent pas
        os.makedirs("output", exist_ok=True)
        os.makedirs("data", exist_ok=True)
    
    def run(self) -> None:
        """Lance l'application en mode interactif."""
        self._print_welcome()
        
        while True:
            self._print_menu()
            choice = input("\nVotre choix : ").strip()
            
            if choice == "1":
                self._load_file()
            elif choice == "2":
                self._compute_and_visualize()
            elif choice == "3":
                self._export_svg()
            elif choice == "4":
                self._export_png()
            elif choice == "5":
                self._analyze_performance()
            elif choice == "6":
                self._show_statistics()
            elif choice == "7":
                print("\nMerci d'avoir utilisé Voronoi Diagram!")
                break
            else:
                print("\n⚠️  Choix invalide. Veuillez réessayer.")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def _print_welcome(self) -> None:
        """Affiche le message de bienvenue."""
        print("=" * 70)
        print(" VORONOI DIAGRAM - APPLICATION ".center(70))
        print("=" * 70)
        print("\nBienvenue dans l'application de génération de diagrammes de Voronoï!")
        print("Cette application vous permet de :")
        print("  • Charger des points depuis un fichier")
        print("  • Calculer et visualiser le diagramme de Voronoï")
        print("  • Exporter vers SVG ou PNG")
        print("  • Analyser les performances de l'algorithme")
        print()
    
    def _print_menu(self) -> None:
        """Affiche le menu principal."""
        print("\n" + "=" * 70)
        print(" MENU PRINCIPAL ".center(70))
        print("=" * 70)
        
        if self._current_file:
            print(f"\n📄 Fichier chargé : {self._current_file}")
        else:
            print("\n📄 Aucun fichier chargé")
        
        if self._current_diagram:
            print(f"📊 Diagramme calculé : {len(self._current_diagram.sites)} sites")
        else:
            print("📊 Aucun diagramme calculé")
        
        print("\nOptions disponibles :")
        print("  1. Charger un fichier de points")
        print("  2. Calculer et visualiser le diagramme")
        print("  3. Exporter en SVG")
        print("  4. Exporter en PNG")
        print("  5. Analyser les performances")
        print("  6. Afficher les statistiques")
        print("  7. Quitter")
    
    def _load_file(self) -> None:
        """Charge un fichier de points."""
        print("\n" + "-" * 70)
        print(" CHARGEMENT DE FICHIER ".center(70))
        print("-" * 70)
        
        # Lister les fichiers disponibles dans data/
        data_dir = "data"
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) if f.endswith(('.txt', '.csv'))]
            if files:
                print(f"\nFichiers disponibles dans '{data_dir}/' :")
                for i, f in enumerate(files, 1):
                    print(f"  {i}. {f}")
                print()
        
        file_path = input("Entrez le chemin du fichier (ou nom si dans data/) : ").strip()
        
        # Si c'est juste un nom de fichier, chercher dans data/
        if not os.path.exists(file_path):
            potential_path = os.path.join("data", file_path)
            if os.path.exists(potential_path):
                file_path = potential_path
        
        try:
            print(f"\n⏳ Chargement du fichier '{file_path}'...")
            points = self._file_reader.read_points_from_file(file_path)
            
            print(f"✅ Fichier chargé avec succès!")
            print(f"   Nombre de points : {len(points)}")
            
            # Afficher quelques points
            if len(points) <= 10:
                print("\n   Points chargés :")
                for i, point in enumerate(points, 1):
                    print(f"     {i}. {point}")
            else:
                print(f"\n   Premiers points :")
                for i, point in enumerate(points[:5], 1):
                    print(f"     {i}. {point}")
                print(f"     ... et {len(points) - 5} autres points")
            
            self._current_file = file_path
            self._current_diagram = None  # Réinitialiser le diagramme
            
        except FileReaderError as e:
            print(f"\n❌ Erreur de lecture : {e}")
        except InvalidFileFormatError as e:
            print(f"\n❌ Format invalide : {e}")
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
    
    def _compute_and_visualize(self) -> None:
        """Calcule et visualise le diagramme."""
        print("\n" + "-" * 70)
        print(" CALCUL ET VISUALISATION ".center(70))
        print("-" * 70)
        
        if not self._current_file:
            print("\n⚠️  Aucun fichier chargé. Veuillez d'abord charger un fichier.")
            return
        
        try:
            # Recharger les points
            print("\n⏳ Chargement des points...")
            points = self._file_reader.read_points_from_file(self._current_file)
            
            # Calculer le diagramme
            print("⏳ Calcul du diagramme de Voronoï...")
            self._current_diagram = self._diagram_builder.build_diagram(points)
            
            print("✅ Diagramme calculé avec succès!")
            
            # Afficher les statistiques
            stats = self._diagram_builder.get_statistics(self._current_diagram)
            print(f"\n   Sites : {stats['num_sites']}")
            print(f"   Arêtes : {stats['num_edges']}")
            print(f"   Sommets : {stats['num_vertices']}")
            
            # Visualiser
            print("\n⏳ Ouverture de la fenêtre de visualisation...")
            self._visualizer.visualize(self._current_diagram)
            
        except DiagramBuilderError as e:
            print(f"\n❌ Erreur de construction : {e}")
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
    
    def _export_svg(self) -> None:
        """Exporte le diagramme en SVG."""
        print("\n" + "-" * 70)
        print(" EXPORT SVG ".center(70))
        print("-" * 70)
        
        if not self._current_diagram:
            print("\n⚠️  Aucun diagramme calculé. Veuillez d'abord calculer un diagramme.")
            return
        
        output_name = input("\nNom du fichier de sortie (sans extension) : ").strip()
        if not output_name:
            output_name = "diagram"
        
        output_path = os.path.join("output", output_name + ".svg")
        
        try:
            print(f"\n⏳ Export vers '{output_path}'...")
            exporter = SVGExporter()
            exporter.export(self._current_diagram, output_path)
            
            print(f"✅ Export réussi!")
            print(f"   Fichier : {output_path}")
            
        except ExporterError as e:
            print(f"\n❌ Erreur d'export : {e}")
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
    
    def _export_png(self) -> None:
        """Exporte le diagramme en PNG."""
        print("\n" + "-" * 70)
        print(" EXPORT PNG ".center(70))
        print("-" * 70)
        
        if not self._current_diagram:
            print("\n⚠️  Aucun diagramme calculé. Veuillez d'abord calculer un diagramme.")
            return
        
        output_name = input("\nNom du fichier de sortie (sans extension) : ").strip()
        if not output_name:
            output_name = "diagram"
        
        output_path = os.path.join("output", output_name + ".png")
        
        try:
            print(f"\n⏳ Export vers '{output_path}'...")
            exporter = ImageExporter()
            exporter.export(self._current_diagram, output_path)
            
            print(f"✅ Export réussi!")
            print(f"   Fichier : {output_path}")
            
        except ExporterError as e:
            print(f"\n❌ Erreur d'export : {e}")
        except Exception as e:
            print(f"\n❌ Erreur inattendue : {e}")
    
    def _analyze_performance(self) -> None:
        """Analyse les performances de l'algorithme."""
        print("\n" + "-" * 70)
        print(" ANALYSE DE PERFORMANCE ".center(70))
        print("-" * 70)
        
        print("\nCette analyse va mesurer le temps d'exécution pour")
        print("différentes tailles de données.")
        print("\nTailles par défaut : 5, 10, 20, 50, 100, 200 points")
        
        custom = input("\nUtiliser des tailles personnalisées ? (o/N) : ").strip().lower()
        
        if custom == 'o':
            sizes_str = input("Entrez les tailles séparées par des virgules : ").strip()
            try:
                sizes = [int(s.strip()) for s in sizes_str.split(',')]
            except ValueError:
                print("\n⚠️  Format invalide. Utilisation des valeurs par défaut.")
                sizes = [5, 10, 20, 50, 100, 200]
        else:
            sizes = [5, 10, 20, 50, 100, 200]
        
        print(f"\n⏳ Analyse en cours pour les tailles : {sizes}")
        print("   (Cela peut prendre quelques instants...)\n")
        
        try:
            analyzer = PerformanceAnalyzer()
            analyzer.analyze_complexity(sizes, num_runs=3)
            analyzer.print_report()
            
            # Sauvegarder les résultats
            output_path = "output/performance_results.csv"
            analyzer.save_results_to_file(output_path)
            
        except Exception as e:
            print(f"\n❌ Erreur lors de l'analyse : {e}")
    
    def _show_statistics(self) -> None:
        """Affiche les statistiques du diagramme actuel."""
        print("\n" + "-" * 70)
        print(" STATISTIQUES DU DIAGRAMME ".center(70))
        print("-" * 70)
        
        if not self._current_diagram:
            print("\n⚠️  Aucun diagramme calculé. Veuillez d'abord calculer un diagramme.")
            return
        
        stats = self._diagram_builder.get_statistics(self._current_diagram)
        
        print("\n📊 Statistiques :")
        print(f"   Nombre de sites : {stats['num_sites']}")
        print(f"   Nombre d'arêtes : {stats['num_edges']}")
        print(f"   Nombre de sommets : {stats['num_vertices']}")
        print(f"   Moyenne arêtes/site : {stats['avg_edges_per_site']:.2f}")
        
        bbox = stats['bounding_box']
        print(f"\n📦 Boîte englobante :")
        print(f"   X : [{bbox[0]:.2f}, {bbox[2]:.2f}]")
        print(f"   Y : [{bbox[1]:.2f}, {bbox[3]:.2f}]")
        print(f"   Largeur : {bbox[2] - bbox[0]:.2f}")
        print(f"   Hauteur : {bbox[3] - bbox[1]:.2f}")


def main():
    """Point d'entrée principal de l'application."""
    try:
        app = VoronoiApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interruption par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()