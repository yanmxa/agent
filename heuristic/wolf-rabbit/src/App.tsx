import React, { useState, useEffect, useRef } from "react";
import { Wolf } from "./simulation/models/wolf";
import { Rabbit } from "./simulation/models/rabbit";
import { Grass } from "./simulation/models/grass";
import { Simulation } from './simulation/simulation';
import { Position } from "./simulation/models/position";
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register necessary chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Define the grid size and cell size
const ROWS = 30;
const COLS = 60;
const CELL_SIZE = 26;  // Cell size for the grid

const App: React.FC = () => {
  const simulation = useRef(new Simulation({ rows: ROWS, cols: COLS }));
  const [grid, setGrid] = useState<(Wolf | Rabbit | Grass | null)[][]>(simulation.current.getGrid());
  const [month, setMonth] = useState<number>(simulation.current.getMonth());
  const [isRunning, setIsRunning] = useState(false); // Track the simulation status
  const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null); // Track the interval
  const [populations, setPopulations] = useState({
    wolves: 0,
    rabbits: 0,
    grass: 0,
  });

  // Explicitly type the chart data state
  const [chartData, setChartData] = useState<{
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      borderColor: string;
      backgroundColor: string;
      fill: boolean;
      tension: number;
      borderWidth: number;
      pointRadius: number; // Set pointRadius to 0 to remove markers
    }[];
  }>({
    labels: [], // Will be filled with months (e.g., "Month 1", "Month 2", etc.)
    datasets: [
      {
        label: 'Wolves',
        data: [], // Populated with wolf count
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 0, // No points shown
      },
      {
        label: 'Rabbits',
        data: [], // Populated with rabbit count
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 0, // No points shown
      },
      {
        label: 'Grass',
        data: [], // Populated with grass count
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.4,
        borderWidth: 3,
        pointRadius: 0, // No points shown
      },
    ],
  });

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

            // Emojis to represent entities
            const emojiSize = 20;
            const centerX = col * CELL_SIZE + CELL_SIZE / 2;
            const centerY = row * CELL_SIZE + CELL_SIZE / 2;

            if (cell instanceof Rabbit) {
              ctx.font = `${emojiSize}px Arial`;
              ctx.fillText("🐇", centerX - emojiSize / 2, centerY + emojiSize / 2);
            } else if (cell instanceof Grass) {
              ctx.font = `${emojiSize}px Arial`;
              ctx.fillText("🌱", centerX - emojiSize / 2, centerY + emojiSize / 2);
            } else if (cell instanceof Wolf) {
              ctx.font = `${emojiSize}px Arial`;
              ctx.fillText("🐺", centerX - emojiSize / 2, centerY + emojiSize / 2);
              // Draw the movement line for the wolf
              // drawLineWithArrow(ctx, cell.previousPosition, cell.position, CELL_SIZE);
            }
          }
        }
      }
    }
  };

  // Function to handle the simulation loop (month increment, update grid, and render)
  const simulateStep = () => {
    simulation.current.next();
    const currentMonth = simulation.current.getMonth();
    const currentGrid = simulation.current.getGrid();
    setMonth(currentMonth);
    setGrid(currentGrid);

    // Track populations
    const wolves = currentGrid.flat().filter(cell => cell instanceof Wolf).length;
    const rabbits = currentGrid.flat().filter(cell => cell instanceof Rabbit).length;
    const grass = currentGrid.flat().filter(cell => cell instanceof Grass).length;

    setPopulations({ wolves, rabbits, grass });

    // Update chart data
    setChartData(prevData => ({
      labels: [...prevData.labels, `${currentMonth}`],
      datasets: prevData.datasets.map(dataset => {
        if (dataset.label === 'Wolves') {
          return { ...dataset, data: [...dataset.data, wolves] };
        } else if (dataset.label === 'Rabbits') {
          return { ...dataset, data: [...dataset.data, rabbits] };
        } else if (dataset.label === 'Grass') {
          return { ...dataset, data: [...dataset.data, grass] };
        }
        return dataset;
      }),
    }));

    drawEntities(currentGrid);
  };

  // Function to start the simulation
  const startSimulation = () => {
    if (!isRunning) {
      setIsRunning(true);
      const id = setInterval(() => {
        simulateStep();
      }, 500); // Adjust speed of simulation (500ms per step)
      setIntervalId(id);
    }
  };

  // Function to stop the simulation
  const stopSimulation = () => {
    if (isRunning && intervalId) {
      clearInterval(intervalId); // Stop the interval
      setIsRunning(false);
      setIntervalId(null); // Reset intervalId
    }
  };

  useEffect(() => {
    drawEntities(simulation.current.getGrid());
  }, []);

  // Chart options for better appearance
  const chartOptions = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: `Population Growth Over Time (Month ${month})`, // Display the month in the title
        font: { size: 18 },
        color: '#333',
      },
      legend: {
        labels: {
          font: { size: 14 },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Months',
          font: { size: 14 },
        },
      },
      y: {
        title: {
          display: true,
          text: 'Population',
          font: { size: 14 },
        },
      },
    },
  };

  return (
<div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-green-200 via-blue-200 to-pink-200 py-10">
  <h1 className="text-3xl font-semibold text-white tracking-wide text-center mb-6">
    Wolf, Rabbit, and Grass Simulation
  </h1>
  
  {/* Canvas and Simulation Controls */}
  <div className="w-full flex flex-col items-center justify-center mb-8">
    <canvas ref={canvasRef} width={COLS * CELL_SIZE} height={ROWS * CELL_SIZE} className="border border-gray-300 shadow-lg rounded-lg bg-white" />
    <div className="text-lg text-white font-medium mt-4">
      Month: {month}
    </div>
  </div>

  {/* Start and Stop Buttons */}
  <div className="flex items-center justify-center space-x-6 mt-4">
    <button
      className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg shadow-md hover:bg-blue-600 hover:shadow-lg transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
      onClick={startSimulation}
    >
      Start
    </button>

    <button
      className="px-6 py-3 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-lg shadow-md hover:bg-red-600 hover:shadow-lg transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
      onClick={stopSimulation}
    >
      Stop
    </button>
  </div>

  {/* Chart displaying population changes */}
  <div className="w-full max-w-3xl mt-10">
    <Line data={chartData} options={chartOptions} />
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
