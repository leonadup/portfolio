import sys
from voronoi.application.file_reader import PointFileReader
from voronoi.application.voronoi_algorithm import VoronoiAlgorithm
from voronoi.infrastructure.svg_exporter import SVGExporter
from voronoi.application.performance import PerformanceAnalyzer

def main():
    if len(sys.argv) != 3:
        print("Usage: python -m src.voronoi.main input.txt output.svg")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    reader = PointFileReader()
    points = reader.read(input_path)

    algorithm = VoronoiAlgorithm()
    polygons = algorithm.compute(points)

    exporter = SVGExporter()
    exporter.export(polygons, points, output_path)

    analyzer = PerformanceAnalyzer()
    execution_time = analyzer.measure(points)

    print(f"Execution time: {execution_time:.6f} seconds")


if __name__ == "__main__":
    main()