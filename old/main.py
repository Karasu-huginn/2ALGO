from solver.column_based import (
    column_based_backtracking,
    column_based_forward_checking,
    column_based_forward_checking_mrv
)
from solver.region_based import (
    region_based_backtracking,
    region_based_forward_checking,
    region_based_forward_checking_mrv
)
from examples.example_grid import GRID, STARS_NUMBER
import time

def validate_solution(grid, stars, k):
    """Valide que la solution respecte toutes les contraintes du jeu"""
    n = len(grid)
    
    # verifie le nombre total d'étoiles
    if len(stars) != n * k:
        return False
    
    # verifie chaque ligne et colonne
    for i in range(n):
        if sum(1 for r, _ in stars if r == i) != k:
            return False
        if sum(1 for _, c in stars if c == i) != k:
            return False
    
    # verifie chaque région
    regions = set(cell for row in grid for cell in row)
    for region in regions:
        if sum(1 for r, c in stars if grid[r][c] == region) != k:
            return False
    
    # verifie les adjacences
    for r, c in stars:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in stars and (dr != 0 or dc != 0):
                    return False
    return True

def print_solution(grid, stars):
    """Affiche la grille avec les étoiles et les régions"""
    n = len(grid)
    for i in range(n):
        row = []
        for j in range(n):
            if (i, j) in stars:
                row.append("★")
            else:
                row.append(f"{grid[i][j]}")
        print(" ".join(row))

#*IA
def benchmark(methods):
    """Compare les performances des différents algorithmes"""
    print("\nBenchmarking...")
    results = []
    for name, method in methods:
        start_time = time.time()
        try:
            stars = method(GRID, STARS_NUMBER)
            valid = validate_solution(GRID, stars, STARS_NUMBER)
            duration = time.time() - start_time
            results.append((name, duration, valid))
            print(f"{name}: {duration:.4f}s - {'Valid' if valid else 'Invalid'}")
        except Exception as e:
            results.append((name, float('inf'), False))
            print(f"{name}: Failed - {str(e)}")
    return results

def main():
    print(f"Grid size : {len(GRID)}x{len(GRID)}, Number of stars : {STARS_NUMBER}")
    
    methods = [
        ("Column-based Backtracking", column_based_backtracking),
        ("Column-based Forward Checking", column_based_forward_checking),
        ("Column-based FC + MRV", column_based_forward_checking_mrv),
        ("Region-based Backtracking", region_based_backtracking),
        ("Region-based Forward Checking", region_based_forward_checking),
        ("Region-based FC + MRV", region_based_forward_checking_mrv),
    ]
    
    for name, method in methods:
        print(f"\nRunning {name}...")
        start_time = time.time()
        try:
            stars = method(GRID, STARS_NUMBER)
            duration = time.time() - start_time
            print_solution(GRID, stars)
            print(f"Valid: {validate_solution(GRID, stars, STARS_NUMBER)}")
            print(f"Time: {duration:.4f} seconds")
        except Exception as e:
            print(f"Error: {str(e)}")
    
 
    benchmark(methods)

if __name__ == "__main__":
    main()

