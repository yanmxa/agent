import random
from context import Context


class Grass:
    def __init__(self, position, ctx: Context = None):
        self.position = position
        self.ctx = ctx
        self.health = 100
        # self.reproduction_rate = 0.7

    # def consume(self):
    #     if self.is_alive:
    #         self.health -= 10  # Each rabbit eats the grass, reducing its health
    #         if self.health <= 0:
    #             self.is_alive = False

    def reproduce(self):
        """Handles the grass reproduction process."""
        row, col = self.position
        grass_cells = []
        barren_cells = []

        # Look for neighboring cells (8 possible directions)
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self.ctx.row_num and 0 <= j < self.ctx.col_num:
                    cell = self.ctx.grid[i][j]
                    if isinstance(cell, Grass):  # Grass cell
                        grass_cells.append((i, j))
                    elif cell is None:  # Barren cell
                        barren_cells.append((i, j))

        # If there are more than 2 grass cells and at least one barren cell around
        if len(grass_cells) > 2 and barren_cells:
            # Randomly choose a barren cell to become grass
            target_cell = random.choice(barren_cells)
            new = Grass(target_cell, ctx=self.ctx)  # Turn barren cell into grass
            self.ctx.grid[target_cell[0]][target_cell[1]] = new
            return new

        return None  # No reproduction
