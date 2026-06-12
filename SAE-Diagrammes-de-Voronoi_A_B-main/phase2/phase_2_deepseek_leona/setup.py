from setuptools import setup, find_packages

setup(
    name="voronoi-app",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pytest>=8.0.0",
        "matplotlib>=3.8.0",
        "Pillow>=10.1.0",
        "numpy>=1.24.0",
    ],
    author="Votre Équipe",
    description="Application de génération de diagrammes de Voronoï",
    python_requires=">=3.9",
)