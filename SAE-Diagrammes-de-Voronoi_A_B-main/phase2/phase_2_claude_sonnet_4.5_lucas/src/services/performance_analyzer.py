"""
Module d'analyse de performance de l'algorithme.

Ce module fournit des outils pour mesurer et analyser les performances
de l'algorithme de Voronoï en fonction du nombre de points.
"""

import time
import math
from typing import List, Dict, Tuple
from src.domain.point import Point
from src.services.diagram_builder import DiagramBuilder


class PerformanceAnalyzer:
    """
    Analyseur de performance de l'algorithme de Voronoï.
    
    Cette classe mesure le temps d'exécution et la complexité
    de l'algorithme pour différentes tailles d'entrée.
    
    Principles SOLID respectés :
    - Single Responsibility : Analyse de performance uniquement
    """
    
    def __init__(self) -> None:
        """Initialise l'analyseur de performance."""
        self._builder = DiagramBuilder()
        self._results: List[Dict] = []
    
    def analyze_complexity(self, sizes: List[int], 
                          num_runs: int = 3) -> List[Dict]:
        """
        Analyse la complexité de l'algorithme pour différentes tailles.
        
        Args:
            sizes: Liste des tailles d'entrée à tester.
            num_runs: Nombre d'exécutions pour chaque taille (pour moyenner).
            
        Returns:
            Liste de dictionnaires contenant les résultats de mesure.
        """
        self._results = []
        
        for size in sizes:
            print(f"Analyse pour {size} points...")
            
            # Générer des points aléatoires
            points = self._generate_random_points(size)
            
            # Mesurer le temps d'exécution plusieurs fois
            times = []
            for run in range(num_runs):
                start_time = time.perf_counter()
                
                try:
                    self._builder.build_diagram(points)
                    end_time = time.perf_counter()
                    elapsed = end_time - start_time
                    times.append(elapsed)
                except Exception as e:
                    print(f"Erreur lors de l'exécution : {e}")
                    times.append(float('inf'))
            
            # Calculer les statistiques
            valid_times = [t for t in times if t != float('inf')]
            if valid_times:
                avg_time = sum(valid_times) / len(valid_times)
                min_time = min(valid_times)
                max_time = max(valid_times)
            else:
                avg_time = min_time = max_time = float('inf')
            
            result = {
                'size': size,
                'avg_time': avg_time,
                'min_time': min_time,
                'max_time': max_time,
                'num_runs': num_runs,
                'success_rate': len(valid_times) / num_runs
            }
            
            self._results.append(result)
            
            print(f"  Temps moyen : {avg_time:.6f}s")
        
        return self._results
    
    def estimate_complexity_order(self) -> Tuple[str, float]:
        """
        Estime l'ordre de complexité de l'algorithme.
        
        Utilise une régression log-log pour estimer si l'algorithme
        est O(n), O(n log n), O(n²), etc.
        
        Returns:
            Tuple (description, exposant) de la complexité estimée.
        """
        if len(self._results) < 2:
            return ("Données insuffisantes", 0.0)
        
        # Extraire les données valides
        valid_results = [r for r in self._results 
                        if r['avg_time'] != float('inf') and r['avg_time'] > 0]
        
        if len(valid_results) < 2:
            return ("Données insuffisantes", 0.0)
        
        # Régression log-log : log(time) = a + b*log(size)
        n = len(valid_results)
        sum_log_size = sum(math.log(r['size']) for r in valid_results)
        sum_log_time = sum(math.log(r['avg_time']) for r in valid_results)
        sum_log_size_sq = sum(math.log(r['size'])**2 for r in valid_results)
        sum_log_size_time = sum(math.log(r['size']) * math.log(r['avg_time']) 
                               for r in valid_results)
        
        # Calcul de la pente (exposant)
        denominator = n * sum_log_size_sq - sum_log_size**2
        if abs(denominator) < 1e-10:
            return ("Impossible à déterminer", 0.0)
        
        slope = (n * sum_log_size_time - sum_log_size * sum_log_time) / denominator
        
        # Interpréter l'exposant
        if slope < 1.2:
            description = "O(n) - Linéaire"
        elif slope < 1.8:
            description = "O(n log n) - Quasi-linéaire"
        elif slope < 2.5:
            description = "O(n²) - Quadratique"
        elif slope < 3.5:
            description = "O(n³) - Cubique"
        else:
            description = f"O(n^{slope:.1f}) - Polynomiale"
        
        return (description, slope)
    
    def _generate_random_points(self, count: int) -> List[Point]:
        """
        Génère des points aléatoires pour les tests.
        
        Args:
            count: Nombre de points à générer.
            
        Returns:
            Liste de points aléatoires.
        """
        import random
        random.seed(42)  # Pour la reproductibilité
        
        points = []
        for _ in range(count):
            x = random.uniform(0, 100)
            y = random.uniform(0, 100)
            points.append(Point(x, y))
        
        return points
    
    def print_report(self) -> None:
        """Affiche un rapport détaillé des résultats."""
        if not self._results:
            print("Aucun résultat à afficher.")
            return
        
        print("\n" + "="*70)
        print(" RAPPORT D'ANALYSE DE PERFORMANCE ".center(70))
        print("="*70)
        
        print(f"\n{'Taille':<10} {'Temps moyen':<15} {'Min':<12} {'Max':<12} {'Succès':<10}")
        print("-"*70)
        
        for result in self._results:
            size = result['size']
            avg = result['avg_time']
            min_t = result['min_time']
            max_t = result['max_time']
            success = result['success_rate'] * 100
            
            if avg == float('inf'):
                print(f"{size:<10} {'ÉCHEC':<15}")
            else:
                print(f"{size:<10} {avg:<15.6f} {min_t:<12.6f} "
                      f"{max_t:<12.6f} {success:<10.1f}%")
        
        # Estimation de la complexité
        complexity, exponent = self.estimate_complexity_order()
        print("\n" + "-"*70)
        print(f"Complexité estimée : {complexity}")
        print(f"Exposant mesuré : {exponent:.2f}")
        print("="*70 + "\n")
    
    def save_results_to_file(self, file_path: str) -> None:
        """
        Sauvegarde les résultats dans un fichier CSV.
        
        Args:
            file_path: Chemin vers le fichier de sortie.
        """
        if not self._results:
            print("Aucun résultat à sauvegarder.")
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # En-tête
                f.write("size,avg_time,min_time,max_time,success_rate\n")
                
                # Données
                for result in self._results:
                    f.write(f"{result['size']},{result['avg_time']},"
                           f"{result['min_time']},{result['max_time']},"
                           f"{result['success_rate']}\n")
            
            print(f"Résultats sauvegardés dans '{file_path}'")
        except IOError as e:
            print(f"Erreur lors de la sauvegarde : {e}")


def main():
    """
    Point d'entrée pour l'analyse de performance en ligne de commande.
    """
    print("Analyse de performance de l'algorithme de Voronoï")
    print("="*50)
    
    analyzer = PerformanceAnalyzer()
    
    # Tailles à tester
    sizes = [5, 10, 20, 50, 100, 200]
    
    # Lancer l'analyse
    analyzer.analyze_complexity(sizes, num_runs=3)
    
    # Afficher le rapport
    analyzer.print_report()
    
    # Sauvegarder les résultats
    analyzer.save_results_to_file("output/performance_results.csv")


if __name__ == "__main__":
    main()