import { Context } from './context';
import { Position } from './position';

export class Grass {
  ctx: Context;
  position: Position;
  health: number;

  constructor(ctx: Context, position: Position) {
    this.position = new Position(position.row, position.col);
    this.ctx = ctx;
    this.health = 100;
  }

  reproduce(): Grass | null {
    const grassCells: Position[] = [];
    const barrenCells: Position[] = [];

    // Get the neighboring positions in radius 1 (8 directions)
    const neighboringPositions = this.position.getPositionsInRadius(this.ctx, 1);

    // Look for neighboring cells (8 possible directions)
    for (const pos of neighboringPositions) {
      const cell = this.ctx.grid[pos.row][pos.col];
      if (cell instanceof Grass) {  // Grass cell
        grassCells.push(pos);
      } else if (cell === null) {  // Barren cell
        barrenCells.push(pos);
      }
    }

    // If there are more than 2 grass cells and at least one barren cell around
    if (grassCells.length >= 2 && barrenCells.length > 0) {
      // Randomly choose a barren cell to become grass
      const targetCell = barrenCells[Math.floor(Math.random() * barrenCells.length)];
      const newGrass = new Grass(this.ctx, targetCell);  // Turn barren cell into grass
      this.ctx.grid[targetCell.row][targetCell.col] = newGrass;
      return newGrass;
    }

    return null;  // No reproduction
  }
}
