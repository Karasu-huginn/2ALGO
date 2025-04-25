import tkinter as tk
import tkinter.messagebox as messagebox
from solver.column_based import column_based_backtracking
from solver.region_based import region_based_backtracking
from examples.example_grid import grid, k
import math

class StarBattleGUI:
    def __init__(self, master, grid, k):
        self.master = master
        self.grid = grid
        self.k = k
        self.n = len(grid)
        self.stars = set()
        
        self.master.title("Star Battle Solver")
        self.cell_size = 50
        self.colors = [
            "#FF9999", "#99FF99", "#9999FF", 
            "#FFFF99", "#FF99FF", "#99FFFF",
            "#FFCC99", "#CCFF99", "#99CCFF",
            "#FF99CC", "#CC99FF", "#99FFCC"
        ]
        
        self.create_widgets()
        self.draw_grid()
    
    def create_widgets(self):
        """Crée les éléments de l'interface"""
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(padx=10, pady=10)
        
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.n * self.cell_size,
            height=self.n * self.cell_size,
            bg="white",
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        self.solve_column_btn = tk.Button(
            self.button_frame,
            text="Résoudre (Colonnes)",
            command=lambda: self.solve(column_based_backtracking)
        )
        self.solve_column_btn.pack(side=tk.LEFT, padx=5)
        
        self.solve_region_btn = tk.Button(
            self.button_frame,
            text="Résoudre (Régions)",
            command=lambda: self.solve(region_based_backtracking)
        )
        self.solve_region_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            self.button_frame,
            text="Effacer",
            command=self.clear,
            fg="red"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.validate_btn = tk.Button(
            self.button_frame,
            text="Vérifier",
            command=self.validate_solution_gui,
            bg="lightgreen"
        )
        self.validate_btn.pack(side=tk.RIGHT, padx=5)
        
        self.canvas.bind("<Button-1>", self.on_cell_click)
    
    def draw_grid(self):
        """Dessine la grille avec les régions et les étoiles"""
        self.canvas.delete("all")
        
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                region = self.grid[i][j]
                color = self.colors[region % len(self.colors)]
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="black",
                    width=1
                )
                
                self.canvas.create_text(
                    x1 + 5, y1 + 5,
                    text=str(region),
                    anchor="nw",
                    font=("Arial", 8)
                )
                
                if (i, j) in self.stars:
                    self.draw_star(x1, y1, x2, y2)
    
    def draw_star(self, x1, y1, x2, y2):
        """Dessine une étoile dans une case"""
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        radius = min(self.cell_size * 0.35, 20)
        
        points = []
        for i in range(10):
            angle = 2 * math.pi * i / 10 - math.pi / 2
            r = radius if i % 2 == 0 else radius * 0.4
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.extend([x, y])
        
        self.canvas.create_polygon(
            points,
            fill="gold",
            outline="black",
            width=1
        )
    
    def on_cell_click(self, event):
        """Gère le clic sur une cellule pour ajouter/supprimer une étoile"""
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.n and 0 <= col < self.n:
            cell = (row, col)
            if cell in self.stars:
                self.stars.remove(cell)
            else:
                if self.is_valid_position(row, col):
                    self.stars.add(cell)
                else:
                    messagebox.showwarning(
                        "Position invalide",
                        "Cette position viole les règles du jeu"
                    )
            self.draw_grid()
    
    def is_valid_position(self, row, col):
        """Vérifie si une position est valide pour une nouvelle étoile"""
        for r in range(max(0, row-1), min(self.n, row+2)):
            for c in range(max(0, col-1), min(self.n, col+2)):
                if (r, c) in self.stars:
                    return False
        
        
        row_count = sum(1 for r, _ in self.stars if r == row)
        col_count = sum(1 for _, c in self.stars if c == col)
        region_count = sum(1 for r, c in self.stars if self.grid[r][c] == self.grid[row][col])
        
        return (row_count < self.k and 
                col_count < self.k and 
                region_count < self.k)
    
    def solve(self, solver):
        """Résout le puzzle avec l'algorithme spécifié"""
        self.stars = solver(self.grid, self.k)
        self.draw_grid()
        if not self.validate_solution():
            messagebox.showerror(
                "Erreur", 
                "La solution trouvée n'est pas valide!\n"
                "Certaines contraintes ne sont pas respectées."
            )
    
    def validate_solution(self):
        """Valide la solution actuelle"""
        return validate_solution(self.grid, self.stars, self.k)
    
    def validate_solution_gui(self):
        """Affiche le résultat de la validation"""
        if self.validate_solution():
            messagebox.showinfo("Validation", "La solution est valide!")
        else:
            messagebox.showerror(
                "Validation",
                "Solution invalide!\n"
                "Vérifiez que:\n"
                "- Chaque ligne/colonne/région a exactement k étoiles\n"
                "- Aucune étoile n'est adjacente"
            )
    
    def clear(self):
        """Efface toutes les étoiles"""
        self.stars = set()
        self.draw_grid()

def validate_solution(grid, stars, k):
    """Fonction de validation (identique à celle de main.py)"""
    n = len(grid)
    if len(stars) != n * k:
        return False
    
    for i in range(n):
        if sum(1 for r, _ in stars if r == i) != k:
            return False
        if sum(1 for _, c in stars if c == i) != k:
            return False
    
    regions = set(cell for row in grid for cell in row)
    for region in regions:
        if sum(1 for r, c in stars if grid[r][c] == region) != k:
            return False
    
    for r, c in stars:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in stars and (dr != 0 or dc != 0):
                    return False
    return True

if __name__ == "__main__":
    root = tk.Tk()
    app = StarBattleGUI(root, grid, k)
    root.mainloop()