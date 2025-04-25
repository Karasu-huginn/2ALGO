def is_valid_position(grid, stars, row, col, k):
    """Vérifie si une position est valide pour placer une étoile"""
    for r in range(max(0, row-1), min(len(grid), row+2)):
        for c in range(max(0, col-1), min(len(grid), col+2)):
            if (r, c) in stars and (r, c) != (row, col):
                return False
    
    row_count = sum(1 for r, c in stars if r == row)
    if row_count >= k:
        return False
        
    col_count = sum(1 for r, c in stars if c == col)
    if col_count >= k:
        return False
        
    region_count = sum(1 for r, c in stars if grid[r][c] == grid[row][col])
    if region_count >= k:
        return False
    
    return True

def get_region_cells(grid, region):
    """Retourne toutes les cellules d'une région donnée"""
    return [(i, j) for i in range(len(grid)) 
                   for j in range(len(grid)) 
                   if grid[i][j] == region]


# doesn't belong in utils
def count_conflicts(grid, stars, row, col):
    """Compte le nombre de conflits potentiels pour une position"""
    conflicts = 0
    for r in range(max(0, row-1), min(len(grid), row+2)):
        for c in range(max(0, col-1), min(len(grid), col+2)):
            if (r, c) in stars and (r != row or c != col):
                conflicts += 1
    return conflicts