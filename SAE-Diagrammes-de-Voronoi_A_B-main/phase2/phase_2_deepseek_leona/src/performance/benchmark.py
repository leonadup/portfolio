"""
Module pour mesurer les performances de l'algorithme.
"""

import time
import random
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
from src.models.point import Point
from src.algorithms.fortune_algorithm import FortuneAlgorithm


class Benchmark:
    """
    Classe pour mesurer et analyser les performances de l'algorithme.
    
    Cette classe suit le principe de responsabilité unique (SOLID) :
    elle ne s'occupe que des mesures de performance.
    """
    
    def __init__(self, generator: FortuneAlgorithm):
        """
        Initialise le benchmark.
        
        Args:
            generator: Générateur de diagramme à tester
        """
        self.generator = generator
        self.results: Dict[int, List[float]] = {}
    
    def generate_random_points(self, n: int, x_range: tuple = (0, 100), 
                               y_range: tuple = (0, 100)) -> List[Point]:
        """
        Génère une liste de points aléatoires.
        
        Args:
            n: Nombre de points à générer
            x_range: Intervalle pour les coordonnées x (min, max)
            y_range: Intervalle pour les coordonnées y (min, max)
            
        Returns:
            List[Point]: Liste de points aléatoires
        """
        points = []
        for _ in range(n):
            x = random.uniform(x_range[0], x_range[1])
            y = random.uniform(y_range[0], y_range[1])
            points.append(Point(x, y))
        return points
    
    def measure_time(self, points: List[Point], iterations: int = 5) -> float:
        """
        Mesure le temps d'exécution de l'algorithme.
        
        Args:
            points: Liste de points à traiter
            iterations: Nombre d'itérations pour la moyenne
            
        Returns:
            float: Temps moyen en secondes
        """
        times = []
        
        for _ in range(iterations):
            start_time = time.perf_counter()
            self.generator.generate(points)
            end_time = time.perf_counter()
            times.append(end_time - start_time)
        
        return sum(times) / len(times)
    
    def run_benchmark(self, point_counts: List[int], iterations_per_count: int = 5) -> Dict[int, float]:
        """
        Exécute le benchmark pour différentes tailles de points.
        
        Args:
            point_counts: Liste des nombres de points à tester
            iterations_per_count: Nombre d'itérations par taille
            
        Returns:
            Dict[int, float]: Dictionnaire {nombre_points: temps_moyen}
        """
        results = {}
        
        for n in point_counts:
            print(f"Benchmark avec {n} points...")
            points = self.generate_random_points(n)
            avg_time = self.measure_time(points, iterations_per_count)
            results[n] = avg_time
            
            if n not in self.results:
                self.results[n] = []
            self.results[n].append(avg_time)
        
        return results
    
    def plot_results(self, save_path: Optional[str] = None) -> None:
        """
        Affiche un graphique des résultats du benchmark.
        
        Args:
            save_path: Chemin pour sauvegarder le graphique (optionnel)
        """
        if not self.results:
            print("Aucun résultat de benchmark disponible.")
            return
        
        sizes = sorted(self.results.keys())
        times = [sum(self.results[size]) / len(self.results[size]) for size in sizes]
        
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, times, 'bo-', label='Temps mesuré')
        plt.xlabel('Nombre de points')
        plt.ylabel('Temps d\'exécution (secondes)')
        plt.title('Performance de l\'algorithme de Fortune')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Ajout d'une courbe de tendance O(n log n) pour comparaison
        if sizes:
            n_log_n = [n * log_n for n, log_n in zip(sizes, [np.log(n) for n in sizes])]
            # Normalisation
            scale = times[-1] / n_log_n[-1] if n_log_n[-1] > 0 else 1
            trend = [scale * val for val in n_log_n]
            plt.plot(sizes, trend, 'r--', label='O(n log n) (théorique)', alpha=0.7)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur les benchmarks effectués.
        
        Returns:
            Dict[str, Any]: Statistiques calculées
        """
        if not self.results:
            return {"error": "Aucune donnée disponible"}
        
        stats = {}
        for size, times in self.results.items():
            stats[size] = {
                "min": min(times),
                "max": max(times),
                "mean": sum(times) / len(times),
                "std_dev": (sum((t - sum(times) / len(times)) ** 2 for t in times) / len(times)) ** 0.5
            }
        
        return stats
    
    def export_results(self, file_path: str) -> None:
        """
        Exporte les résultats au format CSV.
        
        Args:
            file_path: Chemin du fichier de sortie
        """
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Nombre de points', 'Temps moyen (s)', 'Écart-type', 'Min', 'Max'])
            
            for size, times in sorted(self.results.items()):
                mean_time = sum(times) / len(times)
                std_dev = (sum((t - mean_time) ** 2 for t in times) / len(times)) ** 0.5
                min_time = min(times)
                max_time = max(times)
                
                writer.writerow([size, f"{mean_time:.6f}", f"{std_dev:.6f}", 
                               f"{min_time:.6f}", f"{max_time:.6f}"])


# Import nécessaire pour le tracé
import numpy as np