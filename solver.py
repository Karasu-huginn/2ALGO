from example_grid import GRID, STARS_NUMBER
from utils import COLORS, RESET, BOLD

class Solver:
    def __init__(self):
        self.grid = GRID
        self.stars_grid = [[0] * len(GRID) for i in range(len(GRID))]
        self.stars_number = STARS_NUMBER

    def count_stars(self):
        count = 0
        for row in self.stars_grid:
            for cell in row:
                if cell == '*':
                    count += 1
        return count

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

    def ck_colors(self, x, y):
        count = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.stars_grid[i][j] == "*" and self.grid[i][j] == self.grid[x][y]:
                    count += 1
                if count == 2:
                    return False
        return True
    
    def ck_neighbor(self, x, y):
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i >= len(self.grid) or y+j >= len(self.grid):
                    continue
                if i == 0 and j == 0:
                    continue

                if self.stars_grid[x+i][y+j] == "*":
                    return False
        return True

    def is_placeable(self, x, y):
        if not self.ck_lines(x, y):
            return False
        if not self.ck_colors(x,y):
            return False
        if not self.ck_neighbor(x,y):
            return False
        return True
    
    def __str__(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid)):
                if self.stars_grid[x][y] != "*":
                    print(COLORS[int(self.grid[x][y])]+f"  {RESET}", end="")
                else:
                    print(COLORS[int(self.grid[x][y])]+f"{BOLD}<>{RESET}", end="")
            print()

