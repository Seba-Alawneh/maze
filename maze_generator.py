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
    def get_hex(self) -> str: #.....
        """Return hex representation of cell walls."""
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
    def __init__(self, config: Config) -> None:
        self.width: int = config.WIDTH
        self.height: int = config.HEIGHT
        self.entry: tuple = config.ENTRY
        self.exit: tuple = config.EXIT
        self.perfect: bool = config.PERFECT
        self.output_file: str = config.OUTPUT_FILE  # ← ناقص هذا!
        random.seed(config.SEED)                   # 2. الـ random.seed لازم يكون قبل grid_gen عشان الـ seed يأثر على التوليد.
        self.grid: list[list[Cell]] = self.grid_gen()
    
    def embed_42_pattern(self) -> None:
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
            print("Error: The maze size is too small to include the '42' pattern.")
            return
        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2
        for dy in range(pattern_height):
            for dx in range(pattern_width):
                if pattern[dy][dx] == '1':
                    target_cell = self.grid[start_y + dy][start_x + dx]
                    target_cell.visited = True

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
            removed_count = 0

            # استخدام while لضمان هدم العدد المطلوب من الجدران فعلياً
            while removed_count < extra_wall:
                x: int = random.randint(0, self.width - 1)
                y: int = random.randint(0, self.height - 1)
                current_cell: Cell = self.grid[y][x]
                
                # تجنب المساس بمربعات شعار الـ 42
                if current_cell.get_hex() == 'F':
                    continue

                top = self.check_cell(x, y - 1)
                bottom = self.check_cell(x, y + 1)
                left = self.check_cell(x - 1, y)
                right = self.check_cell(x + 1, y)

                neighbors: list[Cell] = []
                
                # التأكد أن الجار ليس جزءاً من الشعار، وأن الجدار بينهما ما زال مبنياً (True)
                if top and top.get_hex() != 'F' and current_cell.north:
                    neighbors.append(top)
                if bottom and bottom.get_hex() != 'F' and current_cell.south:
                    neighbors.append(bottom)
                if left and left.get_hex() != 'F' and current_cell.west:
                    neighbors.append(left)
                if right and right.get_hex() != 'F' and current_cell.east:
                    neighbors.append(right)

                # إذا وجدنا جدراناً صالحة للهدم، نهدم واحداً عشوائياً ونزيد العداد
                if neighbors:
                    random_neighbor = random.choice(neighbors)
                    self.remove_wall(current_cell, random_neighbor)
                    removed_count += 1
    def generate_maze(self) -> None:
        self.embed_42_pattern()
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

    def export_maze(self, solution: str) -> None: #....
        with open(self.output_file, 'w') as f:
            for row in self.grid:
                line: str = ''.join(cell.get_hex() for cell in row)
                f.write(line + '\n')
            f.write('\n')
            f.write(f'{self.entry[0]},{self.entry[1]}\n')
            f.write(f'{self.exit[0]},{self.exit[1]}\n')
            f.write(solution + '\n')

#if __name__ == "__main__":
  #  c = Cell(0, 0)
   # print(c.get_hex())

    #c.south = False
   # print(c.get_hex())

   # c.north = False
    #c.east = False
   # print(c.get_hex())


#if __name__ == "__main__":
   # from maze_solver import MazeSolver

   # config = Config("config.txt")
   # gen = MazeGenerator(config)
  #  gen.generate_maze()

    # حوّل الـ grid من Cell objects لأرقام hex
  #  int_grid = []
   # for row in gen.grid:
       # int_row = [int(cell.get_hex(), 16) for cell in row]
     #   int_grid.append(int_row)

    # شغّل الـ solver
   # solver = MazeSolver(int_grid, config.ENTRY, config.EXIT)
   # solver.solve()
   # solution = solver.get_path_string()

   # print("The real path:", solution)
  #  print("Number of steps:", len(solution))

   # gen.export_maze(solution)
  #  print("write in maze txt!")
