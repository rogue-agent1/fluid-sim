#!/usr/bin/env python3
"""Fluid Sim - Lattice gas automaton for simple fluid dynamics."""
import sys, random

def init_grid(w, h, density=0.3, seed=42):
    random.seed(seed)
    grid = [[0]*w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if random.random() < density and y > 2 and y < h-3:
                grid[y][x] = random.randint(1, 15)
    for y in range(h):
        grid[y][0] = 15; grid[y][w-1] = 15
    for x in range(w):
        grid[0][x] = 15; grid[h-1][x] = 15
    for y in range(h//3, 2*h//3):
        grid[y][w//3] = 15
    return grid

def step(grid):
    h, w = len(grid), len(grid[0])
    new = [[0]*w for _ in range(h)]
    dirs = [(0,-1),(0,1),(-1,0),(1,0)]
    for y in range(1, h-1):
        for x in range(1, w-1):
            v = grid[y][x]
            if v == 15: new[y][x] = 15; continue
            for bit, (dy, dx) in enumerate(dirs):
                if v & (1 << bit):
                    ny, nx = y+dy, x+dx
                    if 0<=ny<h and 0<=nx<w and grid[ny][nx] != 15:
                        new[ny][nx] |= (1 << bit)
                    else:
                        opp = bit ^ 1
                        new[y][x] |= (1 << opp)
    return new

def render(grid):
    chars = " ░▒▓█"
    lines = []
    for row in grid:
        line = ""
        for v in row:
            if v == 15: line += "█"
            else:
                d = bin(v).count("1")
                line += chars[min(d, len(chars)-1)]
        lines.append(line)
    return "\n".join(lines)

def density_stats(grid):
    total = 0; cells = 0
    for row in grid:
        for v in row:
            if v != 15: total += bin(v).count("1"); cells += 1
    return total / max(cells, 1)

def main():
    w, h = 50, 20
    grid = init_grid(w, h, 0.4)
    print(f"=== Fluid Simulation ({w}x{h}) ===\n")
    for t in range(30):
        grid = step(grid)
        if t % 10 == 0:
            print(f"Step {t} (density={density_stats(grid):.2f}):")
            print(render(grid)); print()

if __name__ == "__main__":
    main()
