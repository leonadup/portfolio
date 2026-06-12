# voronoi_app

## Run
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"

Create points.txt then:
python -m voronoi_app render --input points.txt --output out.svg
