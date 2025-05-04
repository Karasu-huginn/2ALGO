from solver import Solver

class Col_fwd_mrv_ck(Solver):
    def solve(self, row):
        if self.count_stars() == self.stars_number * len(self.grid):     # if stars grid full
            return True
        if row == len(self.grid):    #if end of grid
            return False

        for col_1 in range(len(self.grid)):
            if self.is_placeable(row, col_1):
                self.stars_grid[row][col_1] = "*"
                for col_2 in range(col_1+1, len(self.grid)):
                    if self.is_placeable(row, col_2):
                        self.stars_grid[row][col_2] = "*"
                        if self.solve(row+1):
                            return True
                        self.stars_grid[row][col_2] = 0
                self.stars_grid[row][col_1] = 0

        return False