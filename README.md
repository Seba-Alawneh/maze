*This activity has been created as part of the 42 curriculum by habu-har, salalawn.*

# A-Maze-Ing

## Description

A-Maze-Ing is a Python project that generates, solves, and displays mazes.

The program reads a configuration file and generates a random valid maze based on given parameters. It supports perfect and non-perfect modes and computes the shortest path between entry and exit using BFS.

The maze is displayed in a terminal interface and also saved to an output file.

The goal is to understand maze generation algorithms, graph traversal, and modular Python design.

---

## Instructions

### Requirements
Python 3.10+

### Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
python3 a_maze_ing.py config.txt
```

or
```bash
make run
```

---

## Config Format

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42

---

## Makefile

make install
make run
make debug
make clean
make lint
make lint-strict

---

## Algorithm

- Maze generation: Kruskal / Union-Find (randomized)
- Solver: BFS shortest path

---

## Project Structure

- a_maze_ing.py
- maze_generator.py
- maze_solver.py
- config_loader.py
- TerminalRenderer.py
- mazegen/
- setup.py
- Makefile

## AI Usage

Used only for debugging and review. All code written and understood by team.

---

## Resources

- BFS documentation
- Maze generation theory
- YouTube tutorials
