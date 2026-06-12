import time
from src.models import Point
from src.engine import VoronoiEngine

def test_performance_scaling():
    """Mesure le temps de calcul pour un nombre croissant de points."""
    results = {}
    for n in [10, 50, 100]:
        test_points = [Point(i, i) for i in range(n)]
        engine = VoronoiEngine(test_points)
        
        start = time.perf_counter()
        engine.compute_map(resolution=100)
        end = time.perf_counter()
        
        duration = end - start
        results[n] = duration
        print(f"\nTemps pour {n} points: {duration:.4f}s")
    
    # On vérifie juste que le calcul ne prend pas un temps infini
    assert results[100] < 5.0