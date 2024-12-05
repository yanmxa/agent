// Simulation.ts

import { Rabbit } from './models/rabbit';
import { Grass } from './models/grass';
import { Context } from './models/context';
import { Position } from './models/position';
import { Wolf } from './models/wolf';

export class Simulation {
  grid: any[][];
  gridContext: Context;
  month: number;
  // canvasContext: CanvasRenderingContext2D;
  history: { month: number; wolves: number; rabbits: number; grass: number }[];

  constructor(
    gridSize: { rows: number; cols: number },
  ) {
    this.grid = Array.from({ length: gridSize.rows }, () =>
      Array(gridSize.cols).fill(null)
    );
    this.gridContext = new Context(this.grid)
    this.month = 0;
    this.history = [];
    this.putEntities()
  }

  // Helper function to place entities randomly
  putEntities() {
    const { rows, cols } = this.gridContext
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const pos = new Position(row, col)
        const val = Math.random();
        if (val < 0.02) {
          this.grid[row][col] = new Wolf(this.gridContext, pos);
        } else if (val < 0.3) {
          this.grid[row][col] = new Rabbit(this.gridContext, pos);
        } else if (val < 0.6) {
          this.grid[row][col] = new Grass(this.gridContext, pos);
        }
      }
    }
  }

  next() {
    const rabbits = []
    const grasses = []
    const wolves = []
    const barrens = []

    this.month += 1

    let c1 = 0
    let c2 = 0
    let c3 = 0
    let c4 = 0
    const { rows, cols } = this.gridContext
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const cell = this.grid[row][col];
        if (cell instanceof Rabbit) {
          rabbits.push(cell);
          c2 += 1
        } else if (cell instanceof Grass) {
          grasses.push(cell);
          c3 += 1
        } else if (cell instanceof Wolf) {
          c1 += 1
          wolves.push(cell);
        } else if (cell === null) {
          barrens.push(cell);
          c4 += 1
        }
      }
    }

    console.log("wolf %d + rabbit %d + grass %d + barren %d = %d", c1, c2, c3, c4, c1 + c2 + c3 + c4)

    wolves.forEach(w => {
      w.grow()
      w.move()
      w.breed()
    })

    // rabbits.forEach(r => {
    //   r.grow()
    //   r.move()
    //   r.breed()
    // })

    // grasses.forEach(g => g.reproduce())
  }

  getGrid(): any[][] {
    return this.grid
  }

  getWolves(): Wolf[] {
    return this.grid.flat().filter((cell) => cell instanceof Wolf)
  }

  getRabbits(): Rabbit[] {
    return this.grid.flat().filter((cell) => cell instanceof Rabbit)
  }

  getGrasses(): Grass[] {
    return this.grid.flat().filter((cell) => cell instanceof Grass)
  }

  getMonth(): number {
    return this.month
  }

  // // Draw the entities on the canvas
  // drawGrid(ctx: CanvasRenderingContext2D) {
  //   const CELL_SIZE = 26;
  //   const ROWS = this.grid.length;
  //   const COLS = this.grid[0].length;

  //   for (let row = 0; row < ROWS; row++) {
  //     for (let col = 0; col < COLS; col++) {
  //       const cell = this.grid[row][col];
  //       if (cell instanceof Wolf) {
  //         ctx.drawImage('images/wolf_icon.png', col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE);
  //       } else if (cell instanceof Rabbit) {
  //         ctx.drawImage('images/rabbit_icon.png', col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE);
  //       } else if (cell instanceof Grass) {
  //         ctx.drawImage('images/pasture_icon.png', col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE);
  //       }
  //     }
  //   }
  // }
}
