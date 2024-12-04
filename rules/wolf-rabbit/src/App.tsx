import React, { useState, useEffect, useRef } from "react";
import { Wolf } from "./simulation/models/wolf";
import { Rabbit } from "./simulation/models/rabbit";
import { Grass } from "./simulation/models/grass";
import { Simulation } from './simulation/simulation';
import { Position } from "./simulation/models/position";

// Preload images to avoid creating new Image objects repeatedly
const wolfIcon = '/images/wolf_icon.png';
const rabbitIcon = '/images/rabbit_icon.png';
const grassIcon = '/images/pasture_icon.png';
const barrenIcon = '/images/barren_icon.png';

// Define the grid size and cell size
const ROWS = 30;
const COLS = 60;
const CELL_SIZE = 26;  // Cell size for the grid

const App: React.FC = () => {
  const simulation = useRef(new Simulation({ rows: ROWS, cols: COLS }));
  const [grid, setGrid] = useState<(Wolf | Rabbit | Grass | null)[][]>(simulation.current.getGrid());
  const [month, setMonth] = useState<number>(simulation.current.getMonth());
  const [isRunning, setIsRunning] = useState(false); // Track the simulation status
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Function to render the grid on canvas
  const drawEntities = (grid: any[][]) => {
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext("2d");
      if (ctx) {
        ctx.clearRect(0, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE); // Clear canvas before redrawing
        
        for (let row = 0; row < grid.length; row++) {
          for (let col = 0; col < grid[row].length; col++) {
            const cell = grid[row][col];
            const icon = new Image();
            if (cell instanceof Rabbit) {
              icon.src = rabbitIcon;
              icon.onload = () => ctx.drawImage(icon, col * 26, row * 26, 26, 26);
            } else if (cell instanceof Grass) {
              icon.src = grassIcon;
              icon.onload = () => ctx.drawImage(icon, col * 26, row * 26, 26, 26);
            } else if (cell instanceof Wolf) {
              icon.src = wolfIcon;
              icon.onload = () => ctx.drawImage(icon, col * 26, row * 26, 26, 26);

              drawLineWithArrow(ctx, cell.previousPosition, cell.position, CELL_SIZE)
            }
          }
        }
      }
    }
  };

  // Function to handle the simulation loop (month increment, update grid, and render)
  const simulateStep = () => {
    console.log("simulation....")
    simulation.current.next();
    const currentMonth = simulation.current.getMonth();
    const currentGrid = simulation.current.getGrid();
    setMonth(currentMonth);
    setGrid(currentGrid);
    drawEntities(currentGrid);
  };

  // Function to start the simulation
  const startSimulation = () => {
    setIsRunning(true);
  };

  // Function to stop the simulation
  const stopSimulation = () => {
    setIsRunning(false);
  };

  // Function to handle the "Next" button (single step)
  const nextStep = () => {
    simulateStep();
  };

  // Print the current state of the grid for debugging
  const printGrid = () => {
    console.log("Grid state:", grid);
  };

  useEffect(() => {
    drawEntities(simulation.current.getGrid())
  }, []);  

  drawEntities(simulation.current.getGrid());

  return (
    <div>
      <h1>Wolf, Rabbit, and Grass Simulation</h1>
      <canvas ref={canvasRef} width={COLS * CELL_SIZE} height={ROWS * CELL_SIZE} />
      <div>
        <h2>Month: {month}</h2>
      </div>
      <div>
        <button onClick={startSimulation}>
          Start Simulation
        </button>
        <button onClick={stopSimulation}>
          Stop Simulation
        </button>
        <button onClick={nextStep}>
          Next Step
        </button>
        <button onClick={printGrid}>Print Grid</button>
      </div>
    </div>
  );
};

export default App;

const drawLineWithArrow = (
  ctx: CanvasRenderingContext2D,
  start: Position,
  end: Position,
  cellSize: number
) => {
  const headLength = 10; // Length of the arrowhead

  // Convert from grid to pixel positions
  const startPixel = start.toPixel(cellSize);
  const endPixel = end.toPixel(cellSize);

  // Calculate the angle of the line
  const angle = Math.atan2(endPixel.y - startPixel.y, endPixel.x - startPixel.x);

  // Draw the line
  ctx.beginPath();
  ctx.moveTo(startPixel.x, startPixel.y);
  ctx.lineTo(endPixel.x, endPixel.y);
  ctx.stroke();

  // Draw the arrowhead
  ctx.beginPath();
  ctx.moveTo(endPixel.x, endPixel.y);
  ctx.lineTo(
    endPixel.x - headLength * Math.cos(angle - Math.PI / 6),
    endPixel.y - headLength * Math.sin(angle - Math.PI / 6)
  ); // Left side
  ctx.moveTo(endPixel.x, endPixel.y);
  ctx.lineTo(
    endPixel.x - headLength * Math.cos(angle + Math.PI / 6),
    endPixel.y - headLength * Math.sin(angle + Math.PI / 6)
  ); // Right side
  ctx.stroke();
};