import sys
import shutil
from config_loader import Config
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from TerminalRenderer import TerminalRenderer

# Wall colors
BROWN = "\033[38;5;94m"
PURPLE = "\033[38;5;134m"
PINK = "\033[38;5;218m"
DARK_BLUE = "\033[38;5;19m"
ORANGE = "\033[38;5;137m"
GRAY = "\033[38;5;245m"
CYAN = "\033[96m"
RED = "\033[38;5;196m"
RESET = "\033[0m"

COLORS = [BROWN, PURPLE, PINK, DARK_BLUE, ORANGE, GRAY, CYAN]


def build_maze(config: Config):
    gen = MazeGenerator(config)
    gen.generate_maze()
    int_grid = [[int(cell.get_hex(), 16) for cell in row] for row in gen.grid]
    solver = MazeSolver(int_grid, config.ENTRY, config.EXIT)
    solver.solve()
    return gen, int_grid, solver.get_path_coord(), solver.get_path_string()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = Config(sys.argv[1])

        # Enforce exact size 20x15
        if config.WIDTH != 20 or config.HEIGHT != 15:
            raise ValueError("Maze size must be exactly WIDTH=20, HEIGHT=15")

        gen, int_grid, solution_coord, solution = build_maze(config)

        show_path = True
        current_color = CYAN
        color_index = 0

        while True:
            # Simple terminal size check
            try:
                columns, lines = shutil.get_terminal_size()
                min_w = config.WIDTH * 4 + 10
                min_h = config.HEIGHT * 2 + 15

                if columns < min_w or lines < min_h:
                    print(f"\033[91mTerminal too small ({columns}x{lines})!\033[0m")
                    print(f"Needed: {min_w}x{min_h}")
                    print("Enlarge your terminal and press Enter...")
                    input()
                    continue
            except:
                pass

            render = TerminalRenderer(
                config.WIDTH, config.HEIGHT, int_grid,
                config.EXIT, config.ENTRY,
                solution_coord if show_path else []
            )
            render.render(current_color)

            if gen.warning:
                print(f"{RED}{gen.warning}{RESET}")

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")

            choice = input("Choice? (1-4): ").strip()

            if choice == "1":
                gen, int_grid, solution_coord, solution = build_maze(config)
                show_path = True

            elif choice == "2":
                show_path = not show_path

            elif choice == "3":
                if color_index == len(COLORS):
                    color_index = 0
                current_color = COLORS[color_index]
                color_index += 1

            elif choice == "4":
                gen.export_maze(solution)
                print(f"Maze saved to {config.OUTPUT_FILE}")
                print(f"Path length: {len(solution)} steps")
                break

            else:
                print("Invalid choice, try again you have to choose [1, 2, 3, 4]")
                input("Press Enter to continue...")

    except ValueError as e:
        print(e)
    except KeyboardInterrupt:
        print("\r\033[K")
        sys.exit(0)


if __name__ == "__main__":
    main()
