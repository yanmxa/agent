import { Context } from './context';


export class Position {
  row: number;
  col: number;

  constructor(row: number, col: number) {
    this.row = row;
    this.col = col;
  }

  toPixel(cellSize: number) {
    return {
      x: this.col * cellSize + cellSize / 2,  // Add half of cellSize to get the center
      y: this.row * cellSize + cellSize / 2   // Add half of cellSize to get the center
    };
  }

  // Method to get neighboring positions within a given radius
  getPositionsInRadius(ctx: Context, radius: number): Position[] {
    const positions: Position[] = [];
    for (let i = this.row - radius; i <= this.row + radius; i++) {
      for (let j = this.col - radius; j <= this.col + radius; j++) {
        if (
          (i !== this.row && j !== this.col) &&
          i >= 0 && i < ctx.rows &&
          j >= 0 && j < ctx.cols
        ) {
          positions.push(new Position(i, j));
        }
      }
    }
    return positions;
  }
}
