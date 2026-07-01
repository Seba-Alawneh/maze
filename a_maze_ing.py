import sys
import random
from config_loader import Config
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from TerminalRenderer import TerminalRenderer

# NOTE: Wall colors for "Rotate maze colors" feature (PDF requirement)
# Green and Yellow are reserved for path and entry/exit markers
BROWN     = "\033[38;5;94m"
PURPLE    = "\033[38;5;93m"
PINK      = "\033[38;5;205m"
DARK_BLUE = "\033[38;5;19m"
ORANGE    = "\033[38;5;208m"
GRAY      = "\033[38;5;245m"
CYAN      = "\033[96m"
RESET     = "\033[0m"

# NOTE: List of colors that can be randomly chosen when user presses 3
COLORS = [BROWN, PURPLE, PINK, DARK_BLUE, ORANGE, GRAY]


# NOTE: Extracted as a separate function so it can be reused
# when user selects "Re-generate a new maze" (option 1)
def build_maze(config: Config):
    """Generate maze, solve it and return all needed data."""
    gen = MazeGenerator(config)
    gen.generate_maze()

    # NOTE: Convert Cell objects to int grid for MazeSolver and TerminalRenderer
    int_grid = []
    for row in gen.grid:
        int_row = [int(cell.get_hex(), 16) for cell in row]
        int_grid.append(int_row)

    solver = MazeSolver(int_grid, config.ENTRY, config.EXIT)
    solver.solve()
    solution = solver.get_path_string()
    solution_coord = solver.get_path_coord()

    return gen, int_grid, solution_coord, solution


def main() -> None:
    """Main entry point for the maze generator."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config_file = sys.argv[1]
        config = Config(config_file)

        # NOTE: Build maze once before entering the interactive loop
        gen, int_grid, solution_coord, solution = build_maze(config)

        # NOTE: Default state - path is shown, default color is cyan
        show_path = True
        current_color = CYAN

        # NOTE: Main interactive loop - keeps running until user selects 4 (Quit)
        while True:
            render = TerminalRenderer(
                config.WIDTH,
                config.HEIGHT,
                int_grid,
                config.EXIT,
                config.ENTRY,
                solution_coord if show_path else []
                # NOTE: If show_path is False, pass empty list to hide the path
            )
            render.render(current_color)

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ").strip()

            if choice == "1":
                # NOTE: Change seed randomly so each regeneration produces a different maze
                gen, int_grid, solution_coord, solution = build_maze(config)
                show_path = True

            elif choice == "2":
                # NOTE: PDF requirement - Show/Hide valid shortest path
                show_path = not show_path

            elif choice == "3":
                # NOTE: PDF requirement - Change maze wall colors
                # Picks a random color from COLORS list (excludes green and yellow)
                current_color = random.choice(COLORS)

            elif choice == "4":
                # NOTE: Save maze to output file before quitting
                gen.export_maze(solution)
                print(f"Maze saved to {config.OUTPUT_FILE}")
                print(f"Path length: {len(solution)} steps")
                break

            else:
                print("Invalid choice, try again.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()