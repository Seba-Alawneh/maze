import random
from typing import Union
from config_loader import Config


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True
        self.visited: bool = False
    # def get_hex(self) -> str:


class MazeGenerator:
    def __init__(self, config: Config) -> None:
        self.width: int = config.WIDTH
        self.height: int = config.HEIGHT
        self.entry: tuple = config.ENTRY
        self.exit: tuple = config.EXIT
        self.perfect: bool = config.PERFECT
        self.grid: list[list[Cell]] = self.grid_gen()
        random.seed(config.SEED)

    def grid_gen(self) -> list[list[Cell]]:
        main_grid: list[list[Cell]] = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            main_grid.append(row)
        return main_grid

    def check_cell(self, x: int, y: int) -> Union[Cell, bool]:
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return False
        return self.grid[y][x]

    def get_unvisited_neighbors(self, cell: Cell) -> Union[Cell, bool]:
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

    def remove_wall(self, current: Cell, next: Cell) -> None:
        dx, dy = current.x - next.x, current.y - next.y
        if dx == 1:
            current.west = False
            next.east = False
        elif dx == -1:
            current.east = False
            next.west = False
        elif dy == 1:
            current.north = False
            next.south = False
        elif dy == -1:
            current.south = False
            next.north = False

    def imperfect_maze(self) -> None:
        extra_wall: int = int((self.width * self.height) * 0.05)
        for _ in range(extra_wall):
            x: int = random.randint(0, self.width - 1)
            y: int = random.randint(0, self.height - 1)
            current_cell: Cell = self.grid[y][x]

            top = self.check_cell(x, y - 1)
            bottom = self.check_cell(x, y + 1)
            left = self.check_cell(x - 1, y)
            right = self.check_cell(x + 1, y)

            neighbors: list[Cell] = []
            if top:
                neighbors.append(top)
            if bottom:
                neighbors.append(bottom)
            if left:
                neighbors.append(left)
            if right:
                neighbors.append(right)

            if neighbors:
                random_neighbor = random.choice(neighbors)
                self.remove_wall(current_cell, random_neighbor)

    def generate_maze(self) -> None:
        entry_point: Cell = self.grid[self.entry[1]][self.entry[0]]
        stack: list[Cell] = []
        current_cell: Cell = entry_point
        current_cell.visited = True
        stack.append(current_cell)

        while stack:
            next_cell = self.get_unvisited_neighbors(current_cell)
            if next_cell:
                next_cell.visited = True
                stack.append(next_cell)
                self.remove_wall(current_cell, next_cell)
                current_cell = next_cell
            else:
                current_cell = stack.pop()

        if not self.perfect:
            self.imperfect_maze()
    # def export_maze(self): هاذ عشان الاوتبوت فايل


