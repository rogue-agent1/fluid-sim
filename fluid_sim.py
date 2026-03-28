#!/usr/bin/env python3
"""fluid_sim - 2D fluid simulation."""
import argparse, math, sys, time

class Fluid:
    def __init__(self, w, h, visc=0.0001, diff=0.0001):
        self.w, self.h = w, h; self.visc = visc; self.diff = diff
        self.density = [[0.0]*w for _ in range(h)]
        self.vx = [[0.0]*w for _ in range(h)]
        self.vy = [[0.0]*w for _ in range(h)]

    def add_density(self, x, y, amount):
        if 0<=x<self.w and 0<=y<self.h: self.density[y][x] += amount

    def add_velocity(self, x, y, ax, ay):
        if 0<=x<self.w and 0<=y<self.h: self.vx[y][x] += ax; self.vy[y][x] += ay

    def diffuse(self, grid, diff, dt):
        a = dt * diff * self.w * self.h
        new = [[0.0]*self.w for _ in range(self.h)]
        for _ in range(4):
            for y in range(1, self.h-1):
                for x in range(1, self.w-1):
                    new[y][x] = (grid[y][x] + a*(new[y-1][x]+new[y+1][x]+new[y][x-1]+new[y][x+1]))/(1+4*a)
        return new

    def advect(self, grid, vx, vy, dt):
        new = [[0.0]*self.w for _ in range(self.h)]
        for y in range(1, self.h-1):
            for x in range(1, self.w-1):
                sx = x - dt*self.w*vx[y][x]
                sy = y - dt*self.h*vy[y][x]
                sx = max(0.5, min(self.w-1.5, sx))
                sy = max(0.5, min(self.h-1.5, sy))
                i0, j0 = int(sx), int(sy)
                s1, t1 = sx-i0, sy-j0
                s0, t0 = 1-s1, 1-t1
                new[y][x] = (s0*(t0*grid[j0][i0]+t1*grid[j0+1][i0]) + s1*(t0*grid[j0][i0+1]+t1*grid[j0+1][i0+1]))
        return new

    def step(self, dt=0.1):
        self.vx = self.diffuse(self.vx, self.visc, dt)
        self.vy = self.diffuse(self.vy, self.visc, dt)
        self.vx = self.advect(self.vx, self.vx, self.vy, dt)
        self.vy = self.advect(self.vy, self.vx, self.vy, dt)
        self.density = self.diffuse(self.density, self.diff, dt)
        self.density = self.advect(self.density, self.vx, self.vy, dt)

    def render(self):
        chars = " ░▒▓█"
        lines = []
        for row in self.density:
            line = ""
            for v in row:
                ci = min(len(chars)-1, int(min(1, v) * (len(chars)-1)))
                line += chars[ci]
            lines.append(line)
        return "\n".join(lines)

def main():
    p = argparse.ArgumentParser(description="2D fluid simulation")
    p.add_argument("-W","--width", type=int, default=60)
    p.add_argument("-H","--height", type=int, default=30)
    p.add_argument("-s","--steps", type=int, default=50)
    a = p.parse_args()
    f = Fluid(a.width, a.height)
    cx, cy = a.width//2, a.height//2
    for dy in range(-2,3):
        for dx in range(-2,3):
            f.add_density(cx+dx, cy+dy, 1.0)
    f.add_velocity(cx, cy, 5.0, 2.0)
    for s in range(a.steps):
        sys.stdout.write(f"\033[2J\033[HFluid step {s}\n")
        print(f.render())
        f.step(0.1)
        if s < 10:
            f.add_density(cx, cy, 0.5)
            f.add_velocity(cx, cy, 2.0*math.sin(s*0.5), 1.0*math.cos(s*0.3))
        time.sleep(0.1)

if __name__ == "__main__": main()
