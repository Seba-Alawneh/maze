import random
from typing import Union
from config_loader import Config


class Cell:
    """Represents a single cell in the maze with its walls and visitation state."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize a new cell with all walls closed."""
        self.x: int = x
        self.y: int = y
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True
        self.visited: bool = False

    def get_hex(self) -> str:
        """Return the hexadecimal representation of the cell's walls.

        Bit mapping:
            North = 1, East = 2, South = 4, West = 8.
        """
        value: int = 0
        if self.north:
            value += 1
        if self.east:
            value += 2
        if self.south:
            value += 4
        if self.west:
            value += 8
        return format(value, 'X')


class MazeGenerator:
    """Generates a maze using the Recursive Backtracker algorithm."""

    def __init__(self, config: Config) -> None:
        """Initialize the maze generator from configuration."""
        self.width: int = config.WIDTH
        self.height: int = config.HEIGHT
        self.entry: tuple[int, int] = config.ENTRY
        self.exit: tuple[int, int] = config.EXIT
        self.perfect: bool = config.PERFECT
        self.output_file: str = config.OUTPUT_FILE
        self.warning: str = ""
        random.seed(config.SEED)
        self.grid: list[list[Cell]] = self.grid_gen()

    def embed_42_pattern(self) -> None:
        """Embed the '42' pattern by marking specific cells as visited."""
        pattern = [
            "100 111",
            "100 001",
            "111 111",
            "001 100",
            "001 111"
        ]
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            self.warning = "WARNING: The maze size is too small to include the '42' pattern."
            return

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        for dy in range(pattern_height):
            for dx in range(pattern_width):
                if pattern[dy][dx] == '1':
                    target_cell = self.grid[start_y + dy][start_x + dx]
                    if (target_cell.x, target_cell.y) == self.entry or (target_cell.x, target_cell.y) == self.exit:
                        raise ValueError("Error: '42' pattern overlaps with ENTRY or EXIT points!")
                    target_cell.visited = True

    def grid_gen(self) -> list[list[Cell]]:
        """Create an empty grid of Cell objects."""
        main_grid: list[list[Cell]] = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            main_grid.append(row)
        return main_grid

    def check_cell(self, x: int, y: int) -> Union[Cell, bool]:
        """Return the cell at (x, y) or False if out of bounds."""
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return False
        return self.grid[y][x]

    def get_unvisited_neighbors(self, cell: Cell) -> Union[Cell, bool]:
        """Return a random unvisited neighbor or False if none exist."""
        neighbors: list[Cell] = []
        x: int = cell.x
        y: int = cell.y

        top = self.check_cell(x, y - 1)
        left = self.check_cell(x - 1, y)
        right = self.check_cell(x + 1, y)
        bottom = self.check_cell(x, y + 1)

        if top and not top.visited:
            neighbors.append(top)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if right and not right.visited:
            neighbors.append(right)

        return random.choice(neighbors) if neighbors else False

    def remove_wall(self, current: Cell, next_cell: Cell) -> None:
        """Remove the wall between two adjacent cells."""
        dx = current.x - next_cell.x
        dy = current.y - next_cell.y

        if dx == 1:
            current.west = False
            next_cell.east = False
        elif dx == -1:
            current.east = False
            next_cell.west = False
        elif dy == 1:
            current.north = False
            next_cell.south = False
        elif dy == -1:
            current.south = False
            next_cell.north = False

    def imperfect_maze(self) -> None:
        """Remove extra walls to make the maze imperfect (add loops)."""
        extra_wall: int = max(1, int((self.width * self.height) * 0.05))
        removed_count = 0

        while removed_count < extra_wall:
            x: int = random.randint(0, self.width - 1)
            y: int = random.randint(0, self.height - 1)
            current_cell: Cell = self.grid[y][x]

            if current_cell.get_hex() == 'F':
                continue

            top = self.check_cell(x, y - 1)
            bottom = self.check_cell(x, y + 1)
            left = self.check_cell(x - 1, y)
            right = self.check_cell(x + 1, y)

            neighbors: list[Cell] = []

            if top and top.get_hex() != 'F' and current_cell.north:
                neighbors.append(top)
            if bottom and bottom.get_hex() != 'F' and current_cell.south:
                neighbors.append(bottom)
            if left and left.get_hex() != 'F' and current_cell.west:
                neighbors.append(left)
            if right and right.get_hex() != 'F' and current_cell.east:
                neighbors.append(right)

            if neighbors:
                random_neighbor = random.choice(neighbors)
                self.remove_wall(current_cell, random_neighbor)
                removed_count += 1

    def generate_maze(self) -> None:
        """Generate the maze using Recursive Backtracker algorithm."""
        self.embed_42_pattern()

        entry_point: Cell = self.grid[self.entry[1]][self.entry[0]]
        stack: list[Cell] = []
        entry_point.visited = True
        stack.append(entry_point)

        while stack:
            current_cell = stack[-1]
            next_cell = self.get_unvisited_neighbors(current_cell)
            if next_cell:
                self.remove_wall(current_cell, next_cell)
                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

        if not self.perfect:
            self.imperfect_maze()

    def export_maze(self, solution: str) -> None:
        """Export the maze to a file in the required format."""
        with open(self.output_file, 'w') as f:
            for row in self.grid:
                line: str = ''.join(cell.get_hex() for cell in row)
                f.write(line + '\n')
            f.write('\n')
            f.write(f'{self.entry[0]},{self.entry[1]}\n')
            f.write(f'{self.exit[0]},{self.exit[1]}\n')
            f.write(solution + '\n')
