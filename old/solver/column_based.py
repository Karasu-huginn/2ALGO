from solver.utils import is_valid_position, count_conflicts
import itertools

# was in backtrack
def column_based_backtracking_place_star(start_col, n, grid, stars, row, star_cols, k):
    for col in range(start_col, n):
        if is_valid_position(grid, stars, row, col, k):
            stars.add((row, col))
            star_cols.append(col)
            
            if len(star_cols) == k:
                if column_based_backtracking_backtrack(row + 1, n, grid, stars, k):
                    return True
                stars.remove((row, col))
                star_cols.pop()
            else:
                if column_based_backtracking_place_star(col + 1, n, grid, stars, row, star_cols, k):
                    return True
                stars.remove((row, col))
                star_cols.pop()
    return False



# was in column_based_backtracking()
def column_based_backtracking_backtrack(row, n, grid, stars, k):
    if row == n:
        return True
    star_cols = []
    return column_based_backtracking_place_star(0, n, grid, stars, row, star_cols, k)

def column_based_backtracking(grid, k):
    n = len(grid)
    stars = set()
    column_based_backtracking_backtrack(0, n, grid, stars, k)
    return stars


# was in column_based_forward_checking()
def column_based_forward_checking_backtrack(row, n, grid, stars, k):
    if row == n:
        return True
        
    for cols in itertools.combinations(domains[row], k):
        valid = True
        for col in cols:
            if not is_valid_position(grid, stars, row, col, k):
                valid = False
                break
                
        if not valid:
            continue
            
        placed = []
        for col in cols:
            stars.add((row, col))
            placed.append(col)
        
        old_domains = [set(d) for d in domains]
        
        for r in range(row+1, n):
            for col in placed:
                if col in domains[r]:
                    domains[r].remove(col)
            
            for col in placed:
                for dc in [-1, 0, 1]:
                    c = col + dc
                    if c in domains[r]:
                        domains[r].remove(c)
        
        if column_based_forward_checking_backtrack(row + 1, n, grid, stars, k):
            return True
    
        for col in placed:
            stars.remove((row, col))
        domains = old_domains
        
    return False

def column_based_forward_checking(grid, k):
    n = len(grid)
    stars = set()
    domains = [set(range(n)) for _ in range(n)]
    return column_based_forward_checking_backtrack(0, n, grid, stars, k)




# was in column_based_forward_checking_mrv()
def get_mrv_row(domains, n):
    """Trouve la ligne avec le minimum de valeurs restantes"""
    min_options = float('inf')
    selected_row = -1
    for row in range(n):
        if 0 < len(domains[row]) < min_options:
            min_options = len(domains[row])
            selected_row = row
    return selected_row

# was in column_based_forward_checking_mrv()
def column_based_forward_checking_mrv_backtrack(domains, n, k, stars, grid):
    if len(stars) == n * k:
        return True
        
    row = get_mrv_row(domains, n)
    if row == -1:
        return False
        
    cols = sorted(domains[row], key=lambda c: count_conflicts(grid, stars, row, c))
    
    for col in cols:
        if is_valid_position(grid, stars, row, col, k):
            stars.add((row, col))
            
            old_domains = [set(d) for d in domains]
            domains[row] = set()  
            
            updates = []
            for r in range(n):
                if r == row:
                    continue
                    
                if col in domains[r]:
                    domains[r].remove(col)
                    updates.append((r, col))

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        r_adj = row + dr
                        c_adj = col + dc
                        if 0 <= r_adj < n and 0 <= c_adj < n and r_adj == r and c_adj in domains[r]:
                            domains[r].remove(c_adj)
                            updates.append((r, c_adj))
            
            if column_based_forward_checking_mrv_backtrack():
                return True
            
            stars.remove((row, col))
            domains = old_domains
    
    return False

def column_based_forward_checking_mrv(grid, k):
    n = len(grid)
    stars = set()
    domains = [set(range(n)) for _ in range(n)]
    return column_based_forward_checking_mrv_backtrack(domains, n, k, stars, grid)

