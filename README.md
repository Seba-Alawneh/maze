*This activity has been created as part of the 42 curriculum by habu-har, salalawn.*

# A-Maze-ing

## Description

**A-Maze-ing** is a terminal-based maze generator and solver written in Python. Given a simple
configuration file (size, entry/exit points, and a few flags), it:

- Procedurally generates a maze on a rectangular grid of cells, each with up to 4 walls
  (North, East, South, West).
- Embeds a fixed **"42"** pattern into the maze as a block of fully-closed, unreachable cells.
- Computes the shortest path between the entry and the exit using a breadth-first search.
- Renders the maze live in the terminal, with the entry (♛), the exit (⚑), the "42" pattern
  (solid blocks), and — on demand — the solution path (green hexagons).
- Lets the user regenerate a new random maze, toggle the solution path on/off, and rotate the
  wall colors, all from a simple menu.
- Exports the generated maze (walls + entry/exit + solution) to a plain-text hexadecimal file.

The goal of the project is to practice procedural generation, graph traversal, clean/reusable
class design, and terminal rendering, while respecting a strict, fully-testable specification.

## Instructions

### Requirements

- Python 3.10+ (uses `list[...]` built-in generics and modern type hints)
- No third-party dependencies for the core program (standard library only)

### Installation

```bash
git clone <this-repository-url>
cd a-maze-ing
make install
```

### Running the program

```bash
make run
```

This is equivalent to:

```bash
python3 a_maze_ing.py config.txt
```

You can point it at any config file:

```bash
python3 a_maze_ing.py path/to/your_config.txt
```

Once running, use the on-screen menu to:

1. Re-generate a new maze
2. Show/Hide the solution path
3. Rotate the maze wall colors
4. Quit

### Debugging

```bash
make debug
```

Launches the program under `pdb` for step-by-step debugging.

### Linting / static checks

```bash
make lint
```

Runs `flake8` and `mypy` over the project.

### Cleaning generated files

```bash
make clean
```

Removes `__pycache__`, `.mypy_cache`, `.pytest_cache`, and other generated artifacts.

## Configuration File Format

The program reads a plain-text `KEY=VALUE` configuration file (see `config.txt` at the root of
this repository for a working default). Lines starting with `#` are comments and blank lines are
ignored.

| Key | Description | Example | Required |
|---|---|---|---|
| `WIDTH` | Maze width, in number of cells | `WIDTH=20` | Yes |
| `HEIGHT` | Maze height, in number of cells | `HEIGHT=15` | Yes |
| `ENTRY` | Entry cell coordinates `x,y` | `ENTRY=0,0` | Yes |
| `EXIT` | Exit cell coordinates `x,y` | `EXIT=19,14` | Yes |
| `OUTPUT_FILE` | Path of the exported maze file | `OUTPUT_FILE=maze.txt` | Yes |
| `PERFECT` | Whether the maze must have exactly one path between entry and exit | `PERFECT=True` | Yes |
| `SEED` | Optional RNG seed, for reproducible mazes | `SEED=555` | No (defaults to random) |

Validation performed on load:

- All 6 mandatory keys above must be present, or the program raises a clear error.
- `WIDTH` and `HEIGHT` must be strictly positive integers.
- `ENTRY` and `EXIT` must be different, valid `x,y` coordinates strictly inside the maze bounds.
- `OUTPUT_FILE` must not be empty.

### Output file format

The maze is exported as one hexadecimal digit per cell (row by row), where each bit of the digit
encodes a closed wall: `1`=North, `2`=East, `4`=South, `8`=West (added together). After the grid,
a blank line separates it from the entry coordinates, the exit coordinates, and finally the
solution path as a string of direction letters (e.g. `SSSEEN...`).

## Screenshots

The solution path (green) now stays short and thin, leaving the "42" pattern clearly readable
in every generated maze — this was the main bug fixed during development (see
[Maze Generation Algorithm](#maze-generation-algorithm) below).

**Solution path shown** — entry (♛) top-left, exit (⚑) bottom-right, "42" pattern intact:

![Maze with solution path shown](docs/screenshots/maze_with_path.png)

**Solution path hidden** — same maze, toggled off via menu option 2:
![Maze with rotated wall colors](docs/screenshots/maze_rotated_colors.png)


**Wall colors rotated** — via menu option 3:
![Maze with solution path hidden](docs/screenshots/maze_path_hidden.png)


## Maze Generation Algorithm

We use the **Recursive Backtracker** algorithm (a randomized Depth-First Search):

1. Start from the entry cell, mark it as visited, and push it to a stack.
2. While the stack is not empty, peek at the top cell (the current cell).
3. Find all unvisited neighbors of the current cell and pick one at random.
4. If a valid unvisited neighbor exists, remove the wall between the current cell and the neighbor, mark the neighbor as visited, and push it to the stack.
5. If no unvisited neighbors exist (meaning we hit a dead end), pop the current cell from the stack to backtrack to the previous intersection.
6. Stop when the stack is empty — every reachable cell is now connected and part of a single spanning tree.
7. If `PERFECT=False`, an extra ~5% of interior walls are removed afterwards to introduce loops (multiple possible paths), while carefully avoiding the "42" pattern cells.

### Why this algorithm

We implemented the Recursive Backtracker because it is an elegant, stack-based approach that generates classic "perfect" mazes. It is known for producing mazes with a high "river" factor—meaning it creates long, winding corridors and deep dead ends. This makes the maze visually striking and suitably challenging to solve.

One subtlety we had to handle: the "42" pattern cells are embedded before generation starts. We avoid carving into them by ensuring the algorithm checks the wall constraints (`get_hex() != 'F'`) when identifying valid neighbors and applying imperfections, keeping the pattern perfectly intact.



## Reusable Code

The `MazeGenerator` class (in `maze_generator.py`) is fully decoupled from the rendering and
solving logic, and can be reused as a standalone maze-generation library in any other project.

### Basic usage

```python
from config_loader import Config
from maze_generator import MazeGenerator

config = Config("config.txt")          # load and validate a config file
generator = MazeGenerator(config)      # build the (empty) grid
generator.generate_maze()              # carve the maze in place
```

### Custom parameters

Parameters (size, entry/exit, perfect flag, seed) are not passed directly to `MazeGenerator`;
they come from a `Config` object, which can be built from any config file:

```python
config = Config("my_custom_config.txt")   # WIDTH, HEIGHT, ENTRY, EXIT, PERFECT, SEED, ...
generator = MazeGenerator(config)
generator.generate_maze()
```

### Accessing the generated structure and a solution

```python
# The grid is a list of rows of Cell objects, each with .north/.east/.south/.west booleans
int_grid = [[int(cell.get_hex(), 16) for cell in row] for row in generator.grid]

from maze_solver import MazeSolver

solver = MazeSolver(int_grid, generator.entry, generator.exit)
solver.solve()
path_coords = solver.get_path_coord()   # list of (x, y) tuples from entry to exit
path_string = solver.get_path_string()  # e.g. "SSSEEN..."
```

This whole reusable module (code + this documentation) is also packaged as an installable pip
package at the root of this repository: `mazegen-1.0.0-py3-none-any.whl` /
`mazegen-1.0.0.tar.gz`.

## Resources

- [Wikipedia — Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Jamis Buck — "Buckblog": Maze Generation series](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- Python official documentation: [`random`](https://docs.python.org/3/library/random.html),
  [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque)
  (used for BFS in the solver)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

### How AI was used

We used Claude (Anthropic) as a debugging and code-review assistant throughout this project,
specifically for:

- **Diagnosing a visual bug**: the solution path sometimes covered most of the maze, hiding the
  "42" pattern. Claude helped trace this to the choice of generation algorithm (Recursive
  Backtracker) rather than a logic error, by running controlled experiments comparing solution
  path lengths across many random generations.
- **Proposing and implementing the fix**: switching to Randomized Prim's Algorithm, including
  fixing a connectivity regression this introduced (the "42" cells being wrongly treated as real
  connected neighbors), and later simplifying that fix to avoid adding any new class methods or
  attributes.
- **Reviewing the config loader** against the subject's list of mandatory keys, which caught that
  `PERFECT` was missing from the required-keys validation.
- **Auditing docstring coverage** across all classes (`Cell`, `MazeGenerator`, `Config`,
  `TerminalRenderer`) against PEP 257 and writing the missing ones.
- **Drafting this README.md** and the `.gitignore` file.

All AI-suggested changes were reviewed, tested (including automated connectivity/path-length
checks across dozens of random mazes), and understood by us before being committed. The core
program logic, structure, and initial implementation are our own work.

## Team and Project Management

### Roles

- **salalawn**: 
  - **Core Logic & Generation**: Designed and implemented the core maze generation algorithm in `maze_generator.py` using a Randomized Recursive Backtracker.
  - **Pattern & Imperfections**: Built the logic to seamlessly embed the "42" pattern and implemented the `imperfect_maze` function to randomly remove walls and create multiple paths.
  - **UI & Configuration**: Developed the terminal rendering engine (`TerminalRenderer.py`), the configuration loader with strict validation (`config_loader.py`), designed the main configuration file (`config.txt`), and built the interactive main loop (`a_maze_ing.py`).

- **habu-har**: 
  - **Pathfinding & Solver**: Implemented the BFS shortest-path algorithm in `maze_solver.py`.
  - **Packaging & CI**: Handled packaging the reusable module as an installable pip package, creating the `Makefile` (install/run/debug/clean/lint targets), and managing `.gitignore`.
  - **Code Quality & Debugging**: Led the project-wide code-quality pass, adding type hints (`typing` module) to pass `mypy` cleanly, writing PEP 257 docstrings, auditing resource handling[cite: 7], and assisted in debugging and resolving various edge cases.

- **Collaborative Work**:
  - Integration of the solver with the generator and debugging together to ensure the solution path displays correctly without obscuring the "42" pattern.
### Planning

Our initial plan was to split the project cleanly down the middle: one of us owns
generation/solving, the other owns rendering/configuration/CLI, then merge and polish
(README, packaging, linting) together at the end. In practice, the "polish" phase ended
up being much bigger than expected: testing the maze generator against the actual subject
requirements surfaced several issues we hadn't planned for — the solution path sometimes
covering most of the maze, a connectivity bug introduced while fixing that, a missing
mandatory config key (`PERFECT`) not being validated, and gaps in docstring coverage. So
the timeline shifted: less time than expected on the initial generate/render split (which
went smoothly), and more time than expected on debugging, validation, packaging, and
documentation near the end.

### What worked well / what could be improved

What worked well: helping each other out rather than staying strictly in our own lane —
whenever one of us got stuck (or noticed something off in the other's part while testing),
we'd jump in and debug it together instead of waiting. This caught several bugs early
(like the terminal-size handling and the config validation gap) that a stricter split
might have missed until much later.

What could be improved: we left packaging (pip module) and full documentation (README,
docstrings, `.gitignore`) until near the end, which made that final stretch more rushed
than it needed to be. Next time we'd start the Makefile/lint/docstring setup from day one
instead of retrofitting it once the core logic already worked.

### Tools used

- **Git / GitHub** for version control and collaboration.
- **Claude (Anthropic)** as a debugging and code-review assistant (see
  [How AI was used](#how-ai-was-used) above).
- **flake8** and **mypy** for linting and static type checking.
- **pip / build** for packaging the reusable `mazegen` module.
- **make** for standardizing install/run/debug/clean/lint commands.
