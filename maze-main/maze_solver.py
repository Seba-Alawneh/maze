from collections import deque
from typing import Optional


class MazeSolver:
    """Finds the shortest path in a maze using Breadth-First Search (BFS)."""

    DIRECTIONS = {
        'N': (0, -1, 1),   # North: delta_x, delta_y, wall_bit
        'E': (1,  0, 2),   # East
        'S': (0,  1, 4),   # South
        'W': (-1, 0, 8),   # West
    }

    def __init__(
        self,
        grid: list[list[int]],
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        """Initialize the solver with the maze grid and start/end points."""
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self.path: list[str] = []

    def solve(self) -> Optional[list[str]]:
        """Find the shortest path from entry to exit using BFS.

        Returns:
            List of directions (N/E/S/W) if path exists, otherwise None.
        """
        width = len(self.grid[0])
        height = len(self.grid)

        queue: deque[tuple[int, int, list[str]]] = deque()
        queue.append((self.entry[0], self.entry[1], []))

        visited: set[tuple[int, int]] = set()
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
                if self.grid[y][x] & wall:  # Wall is present
                    continue
                if (nx, ny) in visited:
                    continue

                visited.add((nx, ny))
                queue.append((nx, ny, path + [direction]))

        return None

    def get_path_coord(self) -> list[tuple[int, int]]:
        """Convert the path directions into list of (x, y) coordinates."""
        coords: list[tuple[int, int]] = [self.entry]
        x, y = self.entry

        for direction in self.path:
            dx, dy, _ = self.DIRECTIONS[direction]
            x += dx
            y += dy
            coords.append((x, y))

        return coords

    def get_path_string(self) -> str:
        """Return the path as a string of directions (e.g. 'SSSEEN')."""
        return ''.join(self.path)


if __name__ == "__main__":
    # Test with a small fake maze
    fake_grid = [
        [11, 15, 15],
        [10, 15, 15],
        [12,  5,  7],
    ]
    solver = MazeSolver(fake_grid, (0, 0), (2, 2))
    result = solver.solve()

    if result:
        print("Path:", solver.get_path_string())
        print("Number of steps:", len(result))
    else:
        print("No path found")
