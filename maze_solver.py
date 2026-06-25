from collections import deque
from typing import Optional


class MazeSolver:
    """Finds the shortest path in a maze using BFS."""

    DIRECTIONS = {
        'N': (0, -1, 1),
        'E': (1,  0, 2),
        'S': (0,  1, 4),
        'W': (-1, 0, 8),
    }

    def __init__(
        self,
        grid: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Initialize solver with maze grid and entry/exit points."""
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self.path: list[str] = []

    def solve(self) -> Optional[list[str]]:
        """Find shortest path using BFS. Returns list of directions or None."""
        width = len(self.grid[0])
        height = len(self.grid)

        queue: deque = deque()
        queue.append((self.entry[0], self.entry[1], []))

        visited: set = set()
        visited.add(self.entry)

        while queue:
            x, y, path = queue.popleft()

            if (x, y) == self.exit:
                self.path = path
                return path

            for direction, (dx, dy, wall) in self.DIRECTIONS.items():
                nx, ny = x + dx, y + dy

                if not (0 <= nx < width and 0 <= ny < height):
                    continue
                if self.grid[y][x] & wall:
                    continue
                if (nx, ny) in visited:
                    continue

                visited.add((nx, ny))
                queue.append((nx, ny, path + [direction]))

        return None

    def get_path_string(self) -> str:
        """Return path as string of directions (e.g. 'SSSEEN')."""
        return ''.join(self.path)


if __name__ == "__main__":
    fake_grid = [
        [11, 15, 15],
        [10, 15, 15],
        [12,  5,  7],
    ]
    solver = MazeSolver(fake_grid, (0, 0), (2, 2))
    result = solver.solve()
    if result:
        print("path:", solver.get_path_string())
        print("Number of steps:", len(result))
    else:
        print("What's in the path ")
