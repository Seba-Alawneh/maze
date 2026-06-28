from config_loader import Config

class TerminalRenderer:
    def __init__(self, maze_width: int, maze_height: int):
        self.width = maze_width
        self.height = maze_height
        self.canvas_width = (2 * self.width) + 1
        self.canvas_height = (2 * self.height) + 1