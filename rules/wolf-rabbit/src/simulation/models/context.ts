export class Context {
  grid: any[][];
  rows: number;
  cols: number;

  constructor(grid: any[][]) {
    this.grid = grid;
    if (grid.length > 0) {
      this.rows = grid.length;
      if (grid[0].length > 0) {
        this.cols = grid[0].length;
      } else {
        this.cols = 0;  // Handle edge case where rows exist but no columns
      }
    } else {
      this.rows = 0;
      this.cols = 0;  // Handle edge case where the grid is empty
    }
  }
}

