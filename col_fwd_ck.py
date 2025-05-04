from solver import Solver
from utils import print_grid
import time

class Col_fwd_ck(Solver):
    def place_star(self, x, y):
        self.stars_grid[x][y] = "*"
        self.mark_cells(1, x, y)

    def remove_star(self, x, y):
        self.stars_grid[x][y] = 0
        self.mark_cells(-1, x, y)

    def is_placeable(self, x, y):
        if self.mk_hor_grid[x][y] >= 2:
            return False
        if self.mk_vert_grid[x][y] >= 2:
            return False
        if self.mk_reg_grid[x][y] >= 2:
            return False
        if self.mk_nbor_grid[x][y] >= 2:
            return False
        return True

    def solve(self, row):
        if self.count_stars() == self.stars_number * len(self.grid):     # if stars grid full
            return True
        if row == len(self.grid):    #if end of grid
            return False

        for col_1 in range(len(self.grid)):
            if self.is_placeable(row,col_1):
                self.place_star(row, col_1)

                for col_2 in range(col_1+1, len(self.grid)):
                    
                    if self.is_placeable(row,col_2):
                        self.place_star(row, col_2)

                        if self.solve(row+1):
                            return True
                        self.remove_star(row, col_2)
                self.remove_star(row, col_1)

        return False
    


if "__main__" == __name__:
    solver = Col_fwd_ck()
#    solver.test_marker()
#    solver.debug_marker_grids()
    print(solver.solve(0))
    print(solver)













    
    """
    def is_placeable_debug(self, x, y):
        print(self.mk_hor_grid[x][y])
        if self.mk_hor_grid[x][y] >= 2:
            return False
        print(self.mk_vert_grid[x][y])
        if self.mk_vert_grid[x][y] >= 2:
            return False
        print(self.mk_reg_grid[x][y])
        if self.mk_reg_grid[x][y] >= 2:
            return False
        print(self.mk_nbor_grid[x][y])
        if self.mk_nbor_grid[x][y] >= 2:
            return False
        return True
    
    def debug_marker_grids(self):
        print_grid(self.mk_hor_grid)
        print_grid(self.mk_vert_grid)
        print_grid(self.mk_reg_grid)
        print_grid(self.mk_nbor_grid)
        
    def test_marker(self):
        self.place_star(0,4)
        self.place_star(0,6)
        self.place_star(1,1)
        self.place_star(1,9)
        self.place_star(2,3)
        self.place_star(2,7)
        self.place_star(3,5)
        self.place_star(3,9)
        self.place_star(4,1)
        self.place_star(4,3)
        self.place_star(5,5)
        self.place_star(5,8)
        self.place_star(6,0)
        self.place_star(6,2)
        self.place_star(7,4)
        self.place_star(7,7)
        self.place_star(8,0)
        self.place_star(8,2)
        self.place_star(9,6)
        self.place_star(9,8)
        print(self)"""