import sys
from config_loader import Config
from maze_generator import MazeGenerator
from maze_solver import MazeSolver


def main() -> None:
    """Main entry point for the maze generator."""
    if len(sys.argv) != 2:                 #(print) اذا كان عدد مش 2 لما اشغل الملف بطبع الجملة يلي ب
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    # 1. config قرأ الـ
    config = Config(config_file)

    # 2. ولّد المتاهة
    gen = MazeGenerator(config)
    gen.generate_maze()

    #3. solver لأرقام عشان الـ  grid حول
    int_grid = []
    for row in gen.grid:
        int_row = [int(cell.get_hex(), 16) for cell in row]
        int_grid.append(int_row)

    # 4. لاقي أقصر مسار
    solver = MazeSolver(int_grid, config.ENTRY, config.EXIT)
    solver.solve()
    solution = solver.get_path_string()

    # 5. اكتب الملف
    gen.export_maze(solution)
    print(f"Maze saved to {config.OUTPUT_FILE}")
    print(f"Path length: {len(solution)} steps")


if __name__ == "__main__":
    main()
    # (python3 a_maze_ing.py config.txt) لتشغيل الملف اكتبي
    # Usage: python3 a_maze_ing.py config.txt رح يضرب مباشرة و يعطي هاي الجملة (python3 a_maze_ing.py) اذا كتبتي