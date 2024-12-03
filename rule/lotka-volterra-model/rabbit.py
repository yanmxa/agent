import random
from context import Context
from grass import Grass


# Rabbit class
class Rabbit:
    def __init__(self, position, age=0, ctx: Context = None):
        self.age = age
        self.is_alive = True
        self.reproductive_age = 5  # Rabbits breed at 5 months
        self.lifespan = random.randint(12, 36)  # 1 to 3 years
        self.position = position
        self.ctx = ctx
        self.food_intake = 0

    def grow(self):
        """Handles the rabbit's aging process and checks if it is dead."""
        if self.is_alive:
            self.age += 1
            self.food_intake -= 0.1
            if self.age > self.lifespan or self.food_intake < -1:
                self.is_alive = False
                # Replace rabbit's dead cell with grass
                self.ctx.grid[self.position[0]][self.position[1]] = Grass(
                    self.position, self.ctx
                )

    def move(self):
        if not self.is_alive:
            return

        if self.age < self.lifespan * 0.5:  # Young rabbit
            move_chance = 0.4
        elif self.age < self.lifespan * 0.85:  # Middle-aged rabbit
            move_chance = 0.7  # Middle-aged rabbits have more chance to move
        else:  # Older rabbit
            move_chance = 0.2

        if random.random() > move_chance:
            return

        row, col = self.position
        grass_moves = []
        barren_moves = []
        # Look for neighboring cells with grass or barren land
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self.ctx.row_num and 0 <= j < self.ctx.col_num:
                    cell = self.ctx.grid[i][j]
                    if isinstance(cell, Grass):  # Grass cell
                        grass_moves.append((i, j))
                    elif cell is None:  # Barren cell
                        barren_moves.append((i, j))

        # Prefer to move to a grass cell if possible
        if grass_moves:
            target_row, target_col = random.choice(grass_moves)
            # Eat the grass, replace it with barren land
            self.ctx.grid[row][col] = None
            self.ctx.grid[target_row][target_col] = self

            self.food_intake += 0.3
            self.position = (target_row, target_col)
        # If no grass cells, move to a barren cell
        elif barren_moves:
            target_row, target_col = random.choice(barren_moves)
            # Move to the selected barren cell
            self.ctx.grid[row][col] = None
            self.ctx.grid[target_row][target_col] = self

            self.position = (target_row, target_col)

    def breed(self):
        """Handles rabbit breeding based on surrounding grass cells."""
        if self.is_alive and self.age >= self.reproductive_age:

            # Simplified breeding chance based on age
            if self.age < self.lifespan * 0.75:  # Young wolf
                breeding_chance = 0.6
            elif self.age < self.lifespan * 0.9:  # Middle-aged wolf
                breeding_chance = 0.4
            else:  # Older wolf
                breeding_chance = 0.2

            # Increase breeding chance if the rabbit has eaten grass
            if self.food_intake > 0:
                breeding_chance += 0.2  # Increase by 20% if the rabbit has eaten grass
            else:
                breeding_chance -= 0.2

            if random.random() > breeding_chance:
                return None

            # Find surrounding grass cells
            grass_cells = [
                (i, j)
                for i in range(self.position[0] - 1, self.position[0] + 2)
                for j in range(self.position[1] - 1, self.position[1] + 2)
                if 0 <= i < self.ctx.row_num
                and 0 <= j < self.ctx.col_num
                and isinstance(self.ctx.grid[i][j], Grass)
            ]

            # If there are more than 2 grass cells nearby, breed
            if len(grass_cells) > 2:
                # Pick one random grass cell and replace it with a new rabbit
                new_pos = random.choice(grass_cells)
                # Create a new rabbit in the chosen cell
                new_rabbit = Rabbit(new_pos, ctx=self.ctx)
                self.ctx.grid[new_pos[0]][new_pos[1]] = new_rabbit
                return new_rabbit

        return None  # No breeding occurred
