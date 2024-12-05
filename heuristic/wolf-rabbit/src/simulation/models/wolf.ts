import { Context } from './context';
import { Grass } from './grass';
import { Rabbit } from './rabbit';
import { Position } from './position';

export class Wolf {
  previousPosition: Position;
  position: Position;
  age: number;
  isAlive: boolean;
  reproductiveAge: number;
  lifespan: number;
  ctx: Context;
  foodIntake: number;

  constructor(ctx: Context, position: Position, age: number = Math.floor(Math.random() * 96)) {
    this.ctx = ctx;
    this.position = new Position(position.row, position.col);
    this.age = age;
    this.isAlive = true;
    this.reproductiveAge = 24;  // Wolves breed at 2 years (24 months)
    this.lifespan = Math.floor(Math.random() * (96 - 72 + 1)) + 72;  // 6 to 8 years
    this.foodIntake = 0;  // Tracks the number of rabbits eaten, influencing breeding chances
    this.previousPosition = position;
  }

  grow(): void {
    if (this.isAlive) {
      this.age += 1;
      this.foodIntake -= 0.2;
      if (this.age > this.lifespan || this.foodIntake < -1) {
        this.isAlive = false;
        // Replace wolf's dead cell with grass
        this.ctx.grid[this.position.row][this.position.col] = new Grass(this.ctx, this.position);
      }
    }
  }

  goto(position: Position) {
    this.position.col = position.col
    this.position.row = position.row
  }

  move(): void {
    if (!this.isAlive) return;

    const { row, col } = this.position;

    // Collect all neighboring positions in radius 1
    const surroundingCells = this.position.getPositionsInRadius(this.ctx, 1);

    // Initialize cell categories
    let rabbitMoves: Position[] = [];
    let grassMoves: Position[] = [];
    let barrenMoves: Position[] = [];

    // Categorize the neighboring cells
    for (const pos of surroundingCells) {
      const cell = this.ctx.grid[pos.row][pos.col];
      if (cell instanceof Rabbit) {
        rabbitMoves.push(pos);
      } else if (cell instanceof Grass) {
        grassMoves.push(pos);
      } else if (cell === null) {
        barrenMoves.push(pos);
      }
    }

    // Determine movement chance based on wolf's age
    let moveChance = 0.3;  // Default chance for older wolves
    if (this.age < this.lifespan * 0.75) moveChance = 0.7;  // Young wolf
    else if (this.age < this.lifespan * 0.9) moveChance = 0.5;  // Middle-aged wolf

    if (Math.random() < 1) {
      this.ctx.grid[row][col] = new Grass(this.ctx, this.position);  // Replace original position with grass

      this.previousPosition = new Position(row, col)

      // Step 1: Move to a rabbit cell if any exist
      if (rabbitMoves.length > 0) {
        const targetPosition = rabbitMoves[Math.floor(Math.random() * rabbitMoves.length)];
        const { row: targetRow, col: targetCol } = targetPosition;

        this.foodIntake += 0.8;  // Increment food intake as the wolf eats a rabbit
        console.log("Eat rabbit from (%d, %d) to (%d, %d): %f", this.position.row, this.position.col, targetPosition.row, targetPosition.col, this.foodIntake)
        this.goto(targetPosition)
        this.ctx.grid[targetRow][targetCol] = this;  // Move wolf to new position
      }
      // Step 2: If no rabbits, move to a grass cell if any exist
      else if (grassMoves.length > 0) {
        const targetPosition = grassMoves[Math.floor(Math.random() * grassMoves.length)];
        const { row: targetRow, col: targetCol } = targetPosition;

        this.position = targetPosition;
        this.ctx.grid[targetRow][targetCol] = this;  // Move wolf to new position
      }
      // Step 3: If no rabbits or grass, move to a barren cell
      else if (barrenMoves.length > 0) {
        const targetPosition = barrenMoves[Math.floor(Math.random() * barrenMoves.length)];
        const { row: targetRow, col: targetCol } = targetPosition;

        this.position = targetPosition;
        this.ctx.grid[targetRow][targetCol] = this;  // Move wolf to new position
      }
    }
  }


  breed(): Wolf | null {
    if (this.isAlive && this.age >= this.reproductiveAge) {
      let breedingChance = 0.2; // Older wolf
      if (this.age < this.lifespan * 0.75) {
        breedingChance = 0.6;  // Young wolf
      } else if (this.age < this.lifespan * 0.9) {
        breedingChance = 0.4;  // Middle-aged wolf
      }

      // Wolves that have eaten more will have an increased chance to breed
      if (this.foodIntake > 0) {
        breedingChance += 0.1;  // Increase chance by 10% for higher food intake
      } else {
        breedingChance -= 0.5;
      }

      if (Math.random() > breedingChance) {
        return null;
      }

      const row = this.position.row;
      const col = this.position.col;

      // Step 1: Find all neighboring cells with grass or rabbit
      const grassAndRabbitCells: Position[] = this.position
        .getPositionsInRadius(this.ctx, 1) // Get neighboring positions within a radius of 1
        .filter(pos => {
          const cell = this.ctx.grid[pos.row][pos.col];
          return cell instanceof Grass || cell instanceof Rabbit; // Only keep grass or rabbit cells
        });


      // Step 2: If there are not enough grass or rabbit cells, don't breed
      if (grassAndRabbitCells.length < 3) {
        return null;
      }

      // Step 3: Randomly choose one of the neighboring grass/rabbit cells and breed
      const targetCell = grassAndRabbitCells[Math.floor(Math.random() * grassAndRabbitCells.length)];
      const newWolf = new Wolf(this.ctx, new Position(targetCell.row, targetCell.col), 0);
      this.ctx.grid[targetCell.row][targetCell.col] = newWolf;
      return newWolf;
    }

    return null;  // No breeding occurred
  }
}
