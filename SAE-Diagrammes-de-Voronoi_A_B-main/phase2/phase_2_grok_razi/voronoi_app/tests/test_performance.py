# tests/test_performance.py
import pytest
from src.algorithms.voronoi_calculator import VoronoiCalculator


@pytest.mark.slow  # marque le test comme potentiellement long → peut être désactivé avec pytest -m "not slow"
def test_performance_increases_with_n():
    calc = VoronoiCalculator()
    results = calc.measure_performance(max_n=15, trials=2)  # petit test

    prev_time = 0.0
    for n, t in sorted(results.items()):
        assert t > 0, f"Temps nul pour {n} points"
        if n > 5:  # on commence à comparer à partir d'une certaine taille
            assert t >= prev_time * 0.3, \
                f"Temps non croissant ? {n} points → {t:.4f}s (précédent {prev_time:.4f}s)"
        prev_time = t


def test_performance_returns_dict_with_expected_keys():
    calc = VoronoiCalculator()
    results = calc.measure_performance(max_n=9, trials=1)
    assert isinstance(results, dict)
    assert set(results.keys()) == {3,5,7,9}
    assert all(isinstance(v, float) for v in results.values())