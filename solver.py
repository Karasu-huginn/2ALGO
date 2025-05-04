from example_grid import GRID, STARS_NUMBER
from utils import COLORS, RESET, BOLD

class Solver:
    def __init__(self):
        self.grid = GRID
        self.stars_grid = [[0] * len(GRID) for i in range(len(GRID))]
        self.mk_vert_grid = [[0] * len(GRID) for i in range(len(GRID))]
        self.mk_hor_grid = [[0] * len(GRID) for i in range(len(GRID))]
        self.mk_reg_grid = [[0] * len(GRID) for i in range(len(GRID))]
        self.mk_nbor_grid = [[0] * len(GRID) for i in range(len(GRID))]
        self.stars_number = STARS_NUMBER

    def count_stars(self):
        count = 0
        for row in self.stars_grid:
            for cell in row:
                if cell == '*':
                    count += 1
        return count    
    
    def mark_lines(self, value, x, y):
        for i in range(len(self.grid)):
            self.mk_hor_grid[x][i] += value
            self.mk_vert_grid[i][y] += value

    def mark_regions(self, value, x, y):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == self.grid[x][y]:
                    self.mk_reg_grid[i][j] += value
                    
    def mark_neighbors(self, value, x, y):
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i >= len(self.grid) or y+j >= len(self.grid) or x+i < 0 or y+j < 0:
                    continue
                if i == 0 and j == 0:
                    continue
                self.mk_nbor_grid[x+i][y+j] += value
    
    def mark_cells(self, value, x, y):
        self.mark_lines(value, x, y)
        self.mark_regions(value, x, y)
        self.mark_neighbors(value, x, y)

    def ck_lines(self, x, y):
        count_x = 0
        count_y = 0
        for i in range(len(self.grid)):
            if self.stars_grid[x][i] == "*":
                count_y += 1
            if self.stars_grid[i][y] == "*":
                count_x += 1
            if count_x == 2 or count_y == 2:
                return False
        return True

    def ck_regions(self, x, y):
        count = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.stars_grid[i][j] == "*" and self.grid[i][j] == self.grid[x][y]:
                    count += 1
                if count == 2:
                    return False
        return True
    
    def ck_neighbors(self, x, y):
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i >= len(self.grid) or y+j >= len(self.grid) or x+i < 0 or y+j < 0:
                    continue
                if i == 0 and j == 0:
                    continue

                if self.stars_grid[x+i][y+j] == "*":
                    return False
        return True

    def is_placeable(self, x, y):
        if not self.ck_lines(x, y):
            return False
        if not self.ck_regions(x,y):
            return False
        if not self.ck_neighbors(x,y):
            return False
        return True
    
    def __str__(self):
        string = ""
        for x in range(len(self.grid)):
            for y in range(len(self.grid)):
                if self.stars_grid[x][y] == "*":
                    string += COLORS[int(self.grid[x][y])]+f"{BOLD}<>{RESET}"
                else:
                    string += COLORS[int(self.grid[x][y])]+f"  {RESET}"
            string += "\n"
        return string

"""
        for x in range(len(self.grid)):
            for y in range(len(self.grid)):
                if self.stars_grid[x][y] != "*":
                    print(COLORS[int(self.grid[x][y])]+f"  {RESET}", end="")
                else:
                    print(COLORS[int(self.grid[x][y])]+f"{BOLD}<>{RESET}", end="")
            print()
"""