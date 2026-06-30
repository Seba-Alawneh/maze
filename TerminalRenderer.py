from config_loader import Config
import os

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
        self.solution_path = solution_path if solution_path else []

    def clear_screen(self):
        os.system('cls' if os.name == "nt" else 'clear')

    def render(self):
        self.clear_screen()
        height = len(self.grid)
        width = len(self.grid[0])
        color_wall = CYAN
        
        # طباعة السقف العلوي
        print(f"{color_wall}╔{RESET}" + f"{color_wall}═══╦{RESET}" * (width - 1) + f"{color_wall}═══╗{RESET}")
        
        for y in range(height):
            line_cells = f"{color_wall}║{RESET}"
            line_walls = f"{color_wall}╠{RESET}"
            
            for x in range(width):
                cell = self.grid[y][x]

                if (x, y) == self.entry:
                    content = f"{YELLOW} ♛ {RESET}"
                elif (x, y) == self.exit:
                    content = f"{YELLOW} ⚑ {RESET}"
                elif cell == 15:
                    content = f"{color_wall}███{RESET}"
                elif (x, y) in self.solution_path:
                    content = f"{GREEN} ⬢ {RESET}"
                else:
                    content = "   "
                line_cells += content
                
                # فحص الجدار الشرقي
                line_cells += f"{color_wall}║{RESET}" if cell & 2 else " "
                
                # فحص الجدار الجنوبي
                line_walls += f"{color_wall}═══{RESET}" if cell & 4 else "   "
                line_walls += f"{color_wall}╬{RESET}" if x < width - 1 else f"{color_wall}╣{RESET}"
            
            print(line_cells)
            if y != height - 1:
                print(line_walls)
        
        # طباعة الأرضية السفلية
        print(f"{color_wall}╚{RESET}" + f"{color_wall}═══╩{RESET}" * (width - 1) + f"{color_wall}═══╝{RESET}")