import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.io.file_handler import FileHandler
from src.algorithms.voronoi_calculator import VoronoiCalculator
from src.visualization.plotter import VoronoiPlotter

class VoronoiApp:
    """Interface utilisateur principale (Tkinter)."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Diagramme de Voronoï - Phase 1")
        self.root.geometry("900x700")

        self.points = []
        self.diagram = None
        self.calculator = VoronoiCalculator()
        self.plotter = VoronoiPlotter()

        self._build_ui()

    def _build_ui(self):
        tk.Label(self.root, text="Diagramme de Voronoï", font=("Arial", 16, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Charger fichier points", command=self._load_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Calculer & Visualiser", command=self._compute_and_plot).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Exporter SVG", command=self._export_svg).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Exporter PNG", command=self._export_png).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Mesurer performances", command=self._show_performance).pack(side=tk.LEFT, padx=5)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not path:
            return
        try:
            self.points = FileHandler.read_points(path)
            messagebox.showinfo("Succès", f"{len(self.points)} points chargés.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _compute_and_plot(self):
        if not self.points:
            messagebox.showwarning("Attention", "Chargez d'abord un fichier.")
            return
        try:
            self.diagram = self.calculator.compute(self.points)
            fig = self.plotter.plot(self.diagram)
            # Affichage dans Tkinter
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Erreur calcul", str(e))

    def _export_svg(self):
        if not self.diagram:
            messagebox.showwarning("Attention", "Calculez d'abord le diagramme.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".svg")
        if path:
            fig = self.plotter.plot(self.diagram)
            self.plotter.save(fig, path)
            messagebox.showinfo("Export", f"SVG sauvegardé : {path}")

    def _export_png(self):
        if not self.diagram:
            messagebox.showwarning("Attention", "Calculez d'abord le diagramme.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            fig = self.plotter.plot(self.diagram)
            self.plotter.save(fig, path)
            messagebox.showinfo("Export", f"PNG sauvegardé : {path}")

    def _show_performance(self):
        try:
            perf = self.calculator.measure_performance(max_n=25)
            fig, ax = plt.subplots()
            ns = list(perf.keys())
            times = list(perf.values())
            ax.plot(ns, times, 'o-', label="Temps (s)")
            ax.set_xlabel("Nombre de points")
            ax.set_ylabel("Temps (secondes)")
            ax.set_title("Performance de l'algorithme Voronoï")
            ax.grid(True)
            ax.legend()

            # Affichage dans une nouvelle fenêtre
            perf_win = tk.Toplevel(self.root)
            perf_win.title("Mesure performance")
            canvas = FigureCanvasTkAgg(fig, perf_win)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def run(self):
        self.root.mainloop()