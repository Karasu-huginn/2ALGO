from solver import Solver

class Reg_backtrack_ck(Solver):

    def get_cells_region(self, region_id):
        cells = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == region_id:
                    cells.append((i, j))
        return cells

    

    def solve(self, region_id=0):

        region_cells = self.get_cells_region(region_id)
        if self.count_stars() == self.stars_number * len(self.grid):
            return True
        total_regions = len(self.grid)
        if region_id >= total_regions:
            return False


        for i in range(len(region_cells)):
            x1, y1 = region_cells[i]
            if not self.is_placeable(x1, y1):
                continue

            self.stars_grid[x1][y1] = "*"

            for j in range(i+1, len(region_cells)):
                x2, y2 = region_cells[j]
                if not self.is_placeable(x2, y2):
                    continue

                self.stars_grid[x2][y2] = "*"

                if self.solve(region_id + 1):
                    return True

                self.stars_grid[x2][y2] = 0
            self.stars_grid[x1][y1] = 0

        return False
