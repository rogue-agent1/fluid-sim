#!/usr/bin/env python3
"""Simple 2D fluid simulation (lattice gas). Zero dependencies."""
import random, sys

class FluidGrid:
    def __init__(self, width, height):
        self.w, self.h = width, height
        self.density = [[0.0]*width for _ in range(height)]
        self.vx = [[0.0]*width for _ in range(height)]
        self.vy = [[0.0]*width for _ in range(height)]

    def add_source(self, x, y, amount, radius=3):
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.w and 0 <= ny < self.h:
                    d = (dx*dx + dy*dy)**0.5
                    if d <= radius:
                        self.density[ny][nx] += amount * (1 - d/radius)

    def step(self, dt=0.1, diffusion=0.1):
        new_d = [[0.0]*self.w for _ in range(self.h)]
        new_vx = [[0.0]*self.w for _ in range(self.h)]
        new_vy = [[0.0]*self.w for _ in range(self.h)]
        for y in range(1, self.h-1):
            for x in range(1, self.w-1):
                # Diffusion
                lap = (self.density[y-1][x] + self.density[y+1][x] +
                       self.density[y][x-1] + self.density[y][x+1] - 4*self.density[y][x])
                new_d[y][x] = self.density[y][x] + diffusion * lap * dt
                # Advection (simple)
                sx = x - self.vx[y][x] * dt
                sy = y - self.vy[y][x] * dt
                sx = max(0.5, min(self.w-1.5, sx))
                sy = max(0.5, min(self.h-1.5, sy))
                i0, j0 = int(sx), int(sy)
                sf, tf = sx-i0, sy-j0
                if i0+1 < self.w and j0+1 < self.h:
                    new_d[y][x] = (1-sf)*(1-tf)*self.density[j0][i0] + sf*(1-tf)*self.density[j0][i0+1] +                                   (1-sf)*tf*self.density[j0+1][i0] + sf*tf*self.density[j0+1][i0+1]
        self.density = new_d
        self.vx = new_vx
        self.vy = new_vy

    def to_ascii(self, chars=" .:-=+*#%@"):
        mx = max(max(row) for row in self.density)
        if mx <= 0: mx = 1
        lines = []
        for row in self.density:
            line = ""
            for v in row:
                idx = int(v / mx * (len(chars)-1))
                idx = max(0, min(len(chars)-1, idx))
                line += chars[idx]
            lines.append(line)
        return "\n".join(lines)

if __name__ == "__main__":
    g = FluidGrid(40, 20)
    g.add_source(20, 10, 10, 5)
    for _ in range(20):
        g.step(0.1, 0.5)
    print(g.to_ascii())
