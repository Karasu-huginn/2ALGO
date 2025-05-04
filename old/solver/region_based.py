from solver.utils import is_valid_position, count_conflicts, get_region_cells
import itertools

def region_based_backtracking(grid, k):
    n = len(grid)
    regions = set(cell for row in grid for cell in row)
    stars = set()
    
  
    regions_order = sorted(regions, key=lambda r: len(get_region_cells(grid, r)))
    
    def backtrack(region_idx):
        if region_idx == len(regions_order):
            return True
        
        region = regions_order[region_idx]
        cells = get_region_cells(grid, region)
        
        cells = sorted(cells, key=lambda cell: count_conflicts(grid, stars, cell[0], cell[1]))
        
        def place_star(start_idx, stars_placed):
            for i in range(start_idx, len(cells)):
                row, col = cells[i]
                
                if is_valid_position(grid, stars, row, col, k):
                    stars.add((row, col))
                    
                    if stars_placed + 1 == k:  
                        if backtrack(region_idx + 1):
                            return True

                        stars.remove((row, col))
                    else:
                        if place_star(i + 1, stars_placed + 1):
                            return True

                        stars.remove((row, col))
            return False
        
        return place_star(0, 0)
    
    backtrack(0)
    return stars

def region_based_forward_checking(grid, k):
    n = len(grid)
    region_map = {}
    for i in range(n):
        for j in range(n):
            region = grid[i][j]
            if region not in region_map:
                region_map[region] = []
            region_map[region].append((i, j))
    regions = list(region_map.keys())
    stars = set()
    
    def backtrack(region_idx):
        if region_idx == len(regions):
            return True
            
        region = regions[region_idx]
        cells = region_map[region]
        
        for selected in itertools.combinations(cells, k):
            valid = True
            for (r, c) in selected:
                if not is_valid_position(grid, stars, r, c, k):
                    valid = False
                    break
            if not valid:
                continue
                
            for (r, c) in selected:
                stars.add((r, c))
            
            old_region_map = {r: cells.copy() for r, cells in region_map.items()}
            
            for (r, c) in selected:
                for other_region in regions[region_idx+1:]:
                    region_map[other_region] = [
                        (ri, rj) for (ri, rj) in region_map[other_region]
                        if not (abs(ri - r) <= 1 and abs(rj - c) <= 1)
                    ]
            
            if backtrack(region_idx + 1):
                return True
                
            for (r, c) in selected:
                stars.remove((r, c))
            region_map = old_region_map
            
        return False
    
    return backtrack(0)

def region_based_forward_checking_mrv(grid, k):
    n = len(grid)
    region_map = {}
    for i in range(n):
        for j in range(n):
            region = grid[i][j]
            if region not in region_map:
                region_map[region] = []
            region_map[region].append((i, j))
    regions = list(region_map.keys())
    stars = set()
    
    def get_mrv_region():
        """Sélectionne la région avec le minimum de valeurs restantes"""
        non_empty_regions = [r for r in regions if len(region_map[r]) > 0]
        if not non_empty_regions:
            return None
        return min(non_empty_regions, key=lambda r: len(region_map[r]))
    
    def backtrack():
        if len(stars) == n * k:
            return True
            
        region = get_mrv_region()
        if region is None:
            return False
            
        cells = region_map[region]
        
        cells = sorted(cells, key=lambda cell: count_conflicts(grid, stars, cell[0], cell[1]))
        
        for i in range(len(cells)):
            row, col = cells[i]
            
            if is_valid_position(grid, stars, row, col, k):
                stars.add((row, col))
                
                old_region_map = {r: cells.copy() for r, cells in region_map.items()}
                region_map[region] = cells[i+1:]
                
                removed = []
                for other_region in regions:
                    if other_region == region:
                        continue
                    new_cells = []
                    for (ri, rj) in region_map[other_region]:
                        if not (abs(ri - row) <= 1 and abs(rj - col) <= 1):
                            new_cells.append((ri, rj))
                        else:
                            removed.append((other_region, (ri, rj)))
                    region_map[other_region] = new_cells
                
                if backtrack():
                    return True
                
                stars.remove((row, col))
                region_map = old_region_map
                for r, cell in removed:
                    region_map[r].append(cell)
        
        return False
    
    backtrack()
    return stars