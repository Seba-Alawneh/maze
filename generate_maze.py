from config_loader import Config
import random
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False

class MazeGenerator:
    def __init__(self, config: Config):
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.entry = config.ENTRY
        self.exit = config.EXIT
        self.grid =  self.grid_gen()
        random.seed(config.SEED)

    
    def grid_gen(self):
        main_grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(Cell(x, y))
            main_grid.append(row)
        return main_grid
    
    def check_cell(self, x, y):
        if x >= self.width or x<0 or y>= self.height or y<0:
            return False
        return self.grid[y][x]
    
    def get_unvisited_neighbors(self, cell: Cell):
        neighbors = []
        x = cell.x
        y = cell.y

        
        top = self.check_cell(x, y-1)
        left = self.check_cell(x-1, y)
        right = self.check_cell(x+1, y)
        bottom = self.check_cell(x, y+1)
        
        if top and not top.visited:
            neighbors.append(top)
        if left and not left.visited:
            neighbors.append(left)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if right and not right.visited:
            neighbors.append(right)
        return random.choice(neighbors) if neighbors else False
   
    def remove_wall(self, current: Cell, next: Cell):
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
        
    def generate_maze(self):
        entry_point = self.grid[self.entry[1]][self.entry[0]]
        stack = []
        current_cell = entry_point
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
