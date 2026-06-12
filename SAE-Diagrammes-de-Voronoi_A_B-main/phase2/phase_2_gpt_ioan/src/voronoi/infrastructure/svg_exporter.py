from typing import List
from voronoi.domain.polygon import Polygon
from voronoi.domain.point import Point


class SVGExporter:
    """
    Exports Voronoï regions and sites to SVG format
    with automatic scaling and visible points.
    """

    def export(
        self,
        polygons: List[Polygon],
        sites: List[Point],
        filepath: str
    ) -> None:

        # Compute global bounding box
        all_points = [p for poly in polygons for p in poly.vertices]

        min_x = min(p.x for p in all_points)
        max_x = max(p.x for p in all_points)
        min_y = min(p.y for p in all_points)
        max_y = max(p.y for p in all_points)

        width = max_x - min_x
        height = max_y - min_y

        margin = 20

        with open(filepath, "w") as file:
            file.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" '
                f'viewBox="{min_x - margin} {min_y - margin} '
                f'{width + 2*margin} {height + 2*margin}" '
                f'width="800" height="800">\n'
            )

            # Background
            file.write(
                f'<rect x="{min_x - margin}" y="{min_y - margin}" '
                f'width="{width + 2*margin}" '
                f'height="{height + 2*margin}" '
                f'style="fill:white"/>\n'
            )

            # Draw Voronoi cells
            for polygon in polygons:
                if not polygon.vertices:
                    continue

                points_str = " ".join(
                    f"{p.x},{p.y}" for p in polygon.vertices
                )

                file.write(
                    f'<polygon points="{points_str}" '
                    f'style="fill:none;stroke:black;stroke-width:0.5"/>\n'
                )

            # Draw sites (points)
            for site in sites:
                file.write(
                    f'<circle cx="{site.x}" cy="{site.y}" '
                    f'r="1.5" fill="red"/>\n'
                )

            file.write("</svg>")