import os

# NOTE: Green and Yellow are reserved - do NOT use them as wall colors
# Green = solution path marker
# Yellow = entry/exit marker
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


class TerminalRenderer:
    """Renders the maze in the terminal using ASCII art with colors."""

    def __init__(
        self,
        maze_width: int,
        maze_height: int,
        grid: list[list[int]],
        exit_pos: tuple[int, int],
        entry_pos: tuple[int, int],
        solution_path: list[tuple[int, int]] | None = None,
    ) -> None:
        """Initialize the renderer with maze data."""
        self.width = maze_width
        self.height = maze_height
        self.grid = grid
        self.entry = entry_pos
        self.exit = exit_pos
        # If solution_path is empty list, the path is hidden
        self.solution_path = solution_path if solution_path is not None else []

    def clear_screen(self) -> None:
        """Clear the terminal screen (works on Windows and Unix)."""
        os.system('cls' if os.name == "nt" else 'clear')

    def render(self, color: str) -> None:
        """Render the maze with the given wall color."""
        self.clear_screen()
        height = len(self.grid)
        width = len(self.grid[0])
        color_wall = color

        # Top border
        print(f"{color_wall}╔{RESET}" + f"{color_wall}═══╦{RESET}" * (width - 1) + f"{color_wall}═══╗{RESET}")

        for y in range(height):
            line_cells = f"{color_wall}║{RESET}"
            line_walls = f"{color_wall}╠{RESET}"

            for x in range(width):
                cell = self.grid[y][x]

                if (x, y) == self.entry:
                    content = f"{YELLOW} ♛ {RESET}"   # Entry marker
                elif (x, y) == self.exit:
                    content = f"{YELLOW} ⚑ {RESET}"    # Exit marker
                elif cell == 15:  # All walls closed (used for '42' pattern)
                    content = f"{color_wall}███{RESET}"
                elif (x, y) in self.solution_path:
                    content = f"{GREEN} ⬢ {RESET}"     # Solution path
                else:
                    content = "   "

                line_cells += content

                # East wall
                line_cells += f"{color_wall}║{RESET}" if cell & 2 else " "

                # South wall
                line_walls += f"{color_wall}═══{RESET}" if cell & 4 else "   "
                line_walls += f"{color_wall}╬{RESET}" if x < width - 1 else f"{color_wall}╣{RESET}"

            print(line_cells)
            if y != height - 1:
                print(line_walls)

        # Bottom border
        print(f"{color_wall}╚{RESET}" + f"{color_wall}═══╩{RESET}" * (width - 1) + f"{color_wall}═══╝{RESET}")