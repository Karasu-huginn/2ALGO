from solver import Solver

class Reg_fwd_ck(Solver):
    def get_cells_region(self, region_id):
        cells = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == region_id:
                    cells.append((i, j))
        return cells

    #check qu'une regin a assez de cases dispo
    def has_enough_valid_positions(self, region_id):
        count = 0
        for x, y in self.get_cells_region(region_id):
            if self.is_placeable(x, y):
                count += 1
            if count >= self.stars_number:
                return True
        return False

    #check toutes les prochaines regions avec la fonction d'avant
    def check_next_regions(self, next_region_id):
        for r in range(next_region_id, len(self.grid)):
            if not self.has_enough_valid_positions(r):
                return False
        return True

    def solve(self, region_id=0):

        region_cells = self.get_cells_region(region_id)
        if self.count_stars() == self.stars_number * len(self.grid):
            return True
        total_regions = len(self.grid)
        if region_id >= total_regions:
            return False

        #algo de forward
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

                # nouveau truc
                if self.check_next_regions(region_id + 1):
                    if self.solve(region_id + 1):
                        return True

                self.stars_grid[x2][y2] = 0

            self.stars_grid[x1][y1] = 0

        return False