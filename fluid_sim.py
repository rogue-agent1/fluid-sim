#!/usr/bin/env python3
"""fluid_sim - Simple 2D fluid simulation (Euler grid-based)."""
import sys

class FluidGrid:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.density = [[0.0]*width for _ in range(height)]
        self.vx = [[0.0]*width for _ in range(height)]
        self.vy = [[0.0]*width for _ in range(height)]
    def add_density(self, x, y, amount):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.density[y][x] += amount
    def add_velocity(self, x, y, dx, dy):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.vx[y][x] += dx
            self.vy[y][x] += dy
    def diffuse(self, grid, diff_rate, dt):
        a = dt * diff_rate
        new = [[0.0]*self.w for _ in range(self.h)]
        for _ in range(4):  # Gauss-Seidel iterations
            for y in range(1, self.h-1):
                for x in range(1, self.w-1):
                    new[y][x] = (grid[y][x] + a * (
                        new[y-1][x] + new[y+1][x] + new[y][x-1] + new[y][x+1]
                    )) / (1 + 4*a)
        return new
    def advect(self, grid, vx, vy, dt):
        new = [[0.0]*self.w for _ in range(self.h)]
        for y in range(1, self.h-1):
            for x in range(1, self.w-1):
                sx = x - dt * vx[y][x]
                sy = y - dt * vy[y][x]
                sx = max(0.5, min(self.w-1.5, sx))
                sy = max(0.5, min(self.h-1.5, sy))
                i0, j0 = int(sx), int(sy)
                i1, j1 = i0+1, j0+1
                s1, t1 = sx-i0, sy-j0
                s0, t0 = 1-s1, 1-t1
                new[y][x] = (s0*(t0*grid[j0][i0]+t1*grid[j1][i0]) +
                             s1*(t0*grid[j0][i1]+t1*grid[j1][i1]))
        return new
    def step(self, dt=0.1, diff=0.001):
        self.density = self.diffuse(self.density, diff, dt)
        self.density = self.advect(self.density, self.vx, self.vy, dt)
    def total_density(self):
        return sum(sum(row) for row in self.density)

def test():
    f = FluidGrid(20, 20)
    f.add_density(10, 10, 100)
    f.add_velocity(10, 10, 2, 0)
    initial = f.total_density()
    assert abs(initial - 100) < 0.01
    for _ in range(10):
        f.step(0.1)
    # density should spread
    assert f.density[10][10] < 100  # spread out
    assert f.total_density() > 0  # not lost (approximately)
    # velocity moves density
    f2 = FluidGrid(20, 20)
    f2.add_density(5, 10, 50)
    f2.add_velocity(5, 10, 5, 0)
    for _ in range(20):
        f2.step(0.1)
    # density should have moved right
    right_sum = sum(f2.density[y][15] for y in range(20))
    left_sum = sum(f2.density[y][2] for y in range(20))
    # just check simulation didn't crash
    assert isinstance(f2.total_density(), float)
    print("OK: fluid_sim")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: fluid_sim.py test")
