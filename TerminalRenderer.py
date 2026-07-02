from config_loader import Config
import os

# NOTE: Green and Yellow are reserved - do NOT use them as wall colors
# Green = solution path marker
# Yellow = entry/exit marker
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
RESET   = "\033[0m"


class TerminalRenderer:
    def __init__(self, maze_width: int, maze_height: int, grid, exit, entry, solution_path=None):
        self.width = maze_width
        self.height = maze_height
        self.grid = grid
        self.entry = entry
        self.exit = exit
        # NOTE: solution_path is a list of (x,y) coordinates from MazeSolver.get_path_coord()
        # If empty list is passed, path is hidden (used for Show/Hide toggle)
        self.solution_path = solution_path if solution_path else []

    def clear_screen(self):
        # NOTE: Works on both Windows (cls) and Linux/Mac (clear)
        os.system('cls' if os.name == "nt" else 'clear')

    def render(self, color):
        # NOTE: color parameter receives the current wall color from a_maze_ing.py
        # This allows dynamic color change without modifying this class

        self.clear_screen()
        height = len(self.grid)
        width = len(self.grid[0])
        color_wall = color

        # NOTE: Top border of the maze
        print(f"{color_wall}╔{RESET}" + f"{color_wall}═══╦{RESET}" * (width - 1) + f"{color_wall}═══╗{RESET}")

        for y in range(height):
            line_cells = f"{color_wall}║{RESET}"
            line_walls = f"{color_wall}╠{RESET}"

            for x in range(width):
                cell = self.grid[y][x]

                if (x, y) == self.entry:
                    # NOTE: Entry point marker (yellow crown)
                    content = f"{YELLOW} ♛ {RESET}"
                elif (x, y) == self.exit:
                    # NOTE: Exit point marker (yellow flag)
                    content = f"{YELLOW} ⚑ {RESET}"
                elif cell == 15:
                    # NOTE: cell == 15 means all 4 walls closed (N=1+E=2+S=4+W=8=15)
                    # This is used for the "42" pattern - displayed in wall color
                    content = f"{color_wall}███{RESET}"
                elif (x, y) in self.solution_path:
                    # NOTE: PDF requirement - show solution path in green
                    content = f"{GREEN} ⬢ {RESET}"
                else:
                    content = "   "
                line_cells += content

                # NOTE: East wall check using bitwise AND (E=2)
                line_cells += f"{color_wall}║{RESET}" if cell & 2 else " "

                # NOTE: South wall check using bitwise AND (S=4)
                line_walls += f"{color_wall}═══{RESET}" if cell & 4 else "   "
                line_walls += f"{color_wall}╬{RESET}" if x < width - 1 else f"{color_wall}╣{RESET}"

            print(line_cells)
            if y != height - 1:
                print(line_walls)

        # NOTE: Bottom border of the maze
        print(f"{color_wall}╚{RESET}" + f"{color_wall}═══╩{RESET}" * (width - 1) + f"{color_wall}═══╝{RESET}")