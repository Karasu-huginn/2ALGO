from solver import Solver
from example_grid import GRID

class Col_fwd_mrv_ck(Solver):

    def place_star(self, x, y):
        self.stars_grid[x][y] = "*"
        self.cols_marked[y] += 1
        region = self.grid[x][y]
        self.regs_marked[region] += 1
        self.mark_neighbors(1, x, y)

    def remove_star(self, x, y):
        self.stars_grid[x][y] = 0
        self.cols_marked[y] -= 1
        region = self.grid[x][y]
        self.regs_marked[region] -= 1
        self.mark_neighbors(-1, x, y)
                    
    def mark_neighbors(self, value, x, y):
        for i in range(-1,2):
            for j in range(-1,2):
                if x+i >= len(self.grid) or y+j >= len(self.grid) or x+i < 0 or y+j < 0:
                    continue
                if i == 0 and j == 0:
                    continue
                self.mk_nbor_grid[x+i][y+j] += value

    def is_placeable(self, x, y):
        if self.cols_marked[y] >= self.stars_number:
            return False
        region = self.grid[x][y]
        if self.regs_marked[region] >= self.stars_number:
            return False
        if self.mk_nbor_grid[x][y] >= 1:
            return False
        return True
    
    def solve(self, row):
        if self.count_stars() == self.stars_number * len(self.grid):     # if stars grid full
            return True
        if row == len(self.grid):    #if end of grid
            return False

        for col_1 in range(len(self.grid)):
            if self.is_placeable(row, col_1):
                self.place_star(row, col_1)

                for col_2 in range(col_1+1, len(self.grid)):
                    if self.is_placeable(row,col_2):
                        self.place_star(row, col_2)

                        if self.solve(row+1):
                            return True
                        self.remove_star(row, col_2)
                self.remove_star(row, col_1)

        return False
    