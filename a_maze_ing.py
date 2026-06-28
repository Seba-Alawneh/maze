import sys
from config_loader import Config
from maze_generator import MazeGenerator
from maze_solver import MazeSolver


def main() -> None:
    """Main entry point for the maze generator."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        config_file = sys.argv[1]

        # 1. configقرأ الـ
        config = Config(config_file)

        # 2. ولّد المتاهة
        gen = MazeGenerator(config)
        gen.generate_maze()

        # 3.solve لي gridحول
        int_grid = []
        for row in gen.grid:
            int_row = [int(cell.get_hex(), 16) for cell in row]
            int_grid.append(int_row)

        # 4. لاقي أقصر مسار
        solver = MazeSolver(int_grid, config.ENTRY, config.EXIT)
        solver.solve()
        solution = solver.get_path_string()

        # 5. اكتب الملف
        gen.export_maze(solution)
        print(f"Maze saved to {config.OUTPUT_FILE}")
        print(f"Path length: {len(solution)} steps")
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()