import random
from context import Context
from grass import Grass
from rabbit import Rabbit


class Wolf:
    def __init__(self, position, age=random.randint(0, 24), ctx: Context = None):
        self.position = position
        self.age = age
        self.is_alive = True
        self.reproductive_age = 24  # Wolves breed at 2 years (24 months)
        self.lifespan = random.randint(72, 96)  # 6 to 8 years
        self.ctx = ctx
        # Tracks the number of rabbits eaten, influencing breeding chances
        self.food_intake = 0

    def grow(self):
        """Handles the wolf's aging process and checks if it is dead."""
        if self.is_alive:
            self.age += 1
            self.food_intake -= 0.2
            if self.age > self.lifespan or self.food_intake < -1:
                self.is_alive = False
                # Replace wolf's dead cell with grass
                self.ctx.grid[self.position[0]][self.position[1]] = Grass(
                    self.position, self.ctx
                )

    def move(self):
        if not self.is_alive:
            return

        """Handles the wolf's movement based on age, food, and available cells."""
        row, col = self.position
        rabbit_moves, grass_moves, barren_moves = [], [], []

        # Look for neighboring cells
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < self.ctx.row_num and 0 <= j < self.ctx.col_num:
                    cell = self.ctx.grid[i][j]
                    if isinstance(cell, Rabbit):  # Rabbit cell
                        rabbit_moves.append((i, j, cell))
                    elif isinstance(cell, Grass):  # Grass cell
                        grass_moves.append((i, j, cell))
                    elif cell is None:  # Barren cell
                        barren_moves.append((i, j))

        # Determine movement chance based on wolf's age
        if self.age < self.lifespan * 0.75:  # Young wolf
            move_chance = 0.7
        elif self.age < self.lifespan * 0.9:  # Middle-aged wolf
            move_chance = 0.5
        else:  # Older wolf
            move_chance = 0.3

        # Move if random chance allows
        if random.random() < move_chance:
            # Change the original to grass
            self.ctx.grid[self.position[0]][self.position[1]] = Grass(
                self.position, self.ctx
            )

            # Step 1: Move to a rabbit cell if any exist
            if rabbit_moves:
                target_row, target_col, target_cell = random.choice(rabbit_moves)
                # Eat the rabbit
                self.food_intake += 1  # Increment food intake as the wolf eats a rabbit

                self.position = (target_row, target_col)
                self.ctx.grid[target_row][target_col] = self

            # Step 2: If no rabbits, move to a grass cell if any exist
            elif grass_moves:
                target_row, target_col, target_cell = random.choice(grass_moves)

                self.position = (target_row, target_col)
                self.ctx.grid[target_row][target_col] = self

            # Step 3: If no rabbits or grass, move to a barren cell
            elif barren_moves:
                target_row, target_col = random.choice(barren_moves)

                self.position = (target_row, target_col)
                self.ctx.grid[target_row][target_col] = self

    def breed(self):
        """Handles wolf breeding based on age, food intake, and random chance."""
        if self.is_alive and self.age >= self.reproductive_age:
            # Simplified breeding chance based on age
            if self.age < self.lifespan * 0.75:  # Young wolf
                breeding_chance = 0.6
            elif self.age < self.lifespan * 0.9:  # Middle-aged wolf
                breeding_chance = 0.4
            else:  # Older wolf
                breeding_chance = 0.2

            # Wolves that have eaten more will have an increased chance to breed
            if self.food_intake > 0:
                breeding_chance += 0.1  # Increase chance by 10% for higher food intake
            else:
                breeding_chance -= 0.5

            # Random chance to breed based on age and food intake
            if random.random() > breeding_chance:
                return None

            row, col = self.position
            grass_and_rabbit_cells = []

            # Step 1: Find all neighboring cells with grass or rabbit
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.ctx.row_num and 0 <= j < self.ctx.col_num:
                        cell = self.ctx.grid[i][j]
                        if isinstance(cell, (Grass, Rabbit)):  # Grass or Rabbit cell
                            grass_and_rabbit_cells.append((i, j))

            # Step 2: If there are not enough grass or rabbit cells, don't breed
            if len(grass_and_rabbit_cells) < 3:
                return None  # Not enough neighboring grass/rabbit cells to breed

            # Step 4: Randomly choose one of the neighboring grass/rabbit cells and breed
            target_cell = random.choice(
                grass_and_rabbit_cells
            )  # Choose randomly from the list
            new = Wolf(
                target_cell, ctx=self.ctx
            )  # Create a new wolf in the chosen cell
            self.ctx.grid[target_cell[0]][target_cell[1]] = new
            return new
