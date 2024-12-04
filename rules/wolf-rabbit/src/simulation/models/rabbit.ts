import { Context } from './context';
import { Grass } from './grass';
import { Position } from './position';

export class Rabbit {
  age: number;
  isAlive: boolean;
  reproductiveAge: number;
  lifespan: number;
  position: Position;
  ctx: Context;
  foodIntake: number;

  constructor(ctx: Context, position: Position, age: number = Math.floor(Math.random() * 36)) {
    this.age = age;
    this.isAlive = true;
    this.reproductiveAge = 5; // Rabbits breed at 5 months
    this.lifespan = Math.floor(Math.random() * (36 - 12 + 1)) + 12; // 1 to 3 years
    this.position = new Position(position.row, position.col);
    this.ctx = ctx;
    this.foodIntake = 0;
  }

  grow(): void {
    if (this.isAlive) {
      this.age += 1;
      this.foodIntake -= 0.1;
      if (this.age > this.lifespan || this.foodIntake < -1) {
        this.isAlive = false;
        // Add a 10% chance for the rabbit to become null
        if (Math.random() < 0.1) {
          this.ctx.grid[this.position.row][this.position.col] = null;
        } else {
          // Replace the rabbit's dead cell with grass
          this.ctx.grid[this.position.row][this.position.col] = new Grass(this.ctx, this.position);
        }
      }
    }
  }

  move(): void {
    if (!this.isAlive) {
      return;
    }

    let moveChance: number;

    if (this.age < this.lifespan * 0.5) {
      moveChance = 0.4; // Young rabbit
    } else if (this.age < this.lifespan * 0.85) {
      moveChance = 0.7; // Middle-aged rabbit
    } else {
      moveChance = 0.2; // Older rabbit
    }

    if (Math.random() > moveChance) {
      return;
    }

    const neighboringPositions = this.position.getPositionsInRadius(this.ctx, 1);
    const grassMoves: Position[] = [];
    const barrenMoves: Position[] = [];

    for (const pos of neighboringPositions) {
      const cell = this.ctx.grid[pos.row][pos.col];
      if (cell instanceof Grass) {
        grassMoves.push(pos);
      } else if (cell === null) {
        barrenMoves.push(pos);
      }
    }

    // Prefer to move to a grass cell if possible
    if (grassMoves.length > 0) {
      const targetPos = grassMoves[Math.floor(Math.random() * grassMoves.length)];

      this.ctx.grid[this.position.row][this.position.col] = null;
      this.ctx.grid[targetPos.row][targetPos.col] = this;

      this.foodIntake += 0.3;
      this.position = targetPos;
    } else if (barrenMoves.length > 0) {     // If no grass cells, move to a barren cell
      const targetPos = barrenMoves[Math.floor(Math.random() * barrenMoves.length)];

      this.ctx.grid[this.position.row][this.position.col] = null;
      this.ctx.grid[targetPos.row][targetPos.col] = this;

      this.position = targetPos;
    }
  }

  breed(): Rabbit | null {
    if (this.isAlive && this.age >= this.reproductiveAge) {
      let breedingChance: number;

      if (this.age < this.lifespan * 0.75) {
        breedingChance = 0.6; // Young rabbit
      } else if (this.age < this.lifespan * 0.9) {
        breedingChance = 0.4; // Middle-aged rabbit
      } else {
        breedingChance = 0.2; // Older rabbit
      }

      // Increase breeding chance if the rabbit has eaten grass
      if (this.foodIntake > 0) {
        breedingChance += 0.2; // Increase by 20% if the rabbit has eaten grass
      } else {
        breedingChance -= 0.2;
      }

      if (Math.random() > breedingChance) {
        return null;
      }

      // Find surrounding grass cells
      const grassCells = this.position.getPositionsInRadius(this.ctx, 1).filter(pos => {
        const cell = this.ctx.grid[pos.row][pos.col];
        return cell instanceof Grass;
      });

      // If there are more than 2 grass cells nearby, breed
      if (grassCells.length > 2) {
        const newPos = grassCells[Math.floor(Math.random() * grassCells.length)];
        const newRabbit = new Rabbit(this.ctx, newPos, 0);
        this.ctx.grid[newPos.row][newPos.col] = newRabbit;
        return newRabbit;
      }
    }

    return null; // No breeding occurred
  }
}
