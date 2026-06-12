from __future__ import annotations
import argparse
from typing import List
from ..infrastructure.parsing import parse_points_file, PointParseError
from ..domain.voronoi import compute_voronoi_diagram
from ..infrastructure.svg_renderer import save_svg
from ..infrastructure.benchmark import run_benchmark, format_benchmark_table

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="voronoi_app", description="Voronoi diagram generator (pure Python) + SVG + bench.")
    sp = p.add_subparsers(dest="command", required=True)

    r = sp.add_parser("render", help="Render Voronoi diagram to SVG.")
    r.add_argument("--input", "-i", required=True)
    r.add_argument("--output", "-o", required=True)

    b = sp.add_parser("bench", help="Benchmark Voronoi computation.")
    b.add_argument("--input", "-i", required=True)
    b.add_argument("--steps", type=int, default=10)
    b.add_argument("--repeat", type=int, default=3)
    return p

def main(argv: List[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        points = parse_points_file(args.input)
    except PointParseError as exc:
        parser.error(str(exc))

    if args.command == "render":
        diagram = compute_voronoi_diagram(points)
        save_svg(diagram, args.output)
        print(f"SVG generated: {args.output}")
    elif args.command == "bench":
        res = run_benchmark(points, steps=args.steps, repeat=args.repeat)
        print(format_benchmark_table(res))
