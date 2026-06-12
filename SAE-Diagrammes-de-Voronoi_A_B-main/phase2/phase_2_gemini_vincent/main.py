import sys
import matplotlib.pyplot as plt
from src.io_handler import FileHandler
from src.engine import VoronoiEngine

# Patch de sécurité pour Python 3.14
sys.setrecursionlimit(2000)

def run_app(filename: str):
    try:
        points = FileHandler.read_points_from_file(filename)
        engine = VoronoiEngine(points, padding=5.0)
        
        print(f"Calcul en cours pour {len(points)} points...")
        voronoi_map, bounds = engine.compute_map(resolution=400)
        
        # Rendu "Lightweight" (Plus de deepcopy)
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(voronoi_map, extent=bounds, origin='lower', cmap='Set3', alpha=0.8)
        
        # Dessin des germes
        ax.scatter([p.x for p in points], [p.y for p in points], c='black', s=15)
        
        ax.set_title("Diagramme de Voronoï - Version Optimisée")
        plt.colorbar(im, label="ID de la cellule")
        plt.show()

    except Exception as e:
        print(f"ERREUR : {e}")

if __name__ == "__main__":
    run_app("data.txt")