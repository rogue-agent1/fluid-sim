#!/usr/bin/env python3
"""Fluid simulation — simplified 2D Navier-Stokes (Stam's stable fluids)."""
import sys, os, time

class Fluid:
    def __init__(self, n=40, diff=0.0001, visc=0.0001, dt=0.1):
        self.n = n; self.diff = diff; self.visc = visc; self.dt = dt
        s = (n+2)**2
        self.d = [0.0]*s; self.d0 = [0.0]*s
        self.u = [0.0]*s; self.v = [0.0]*s
        self.u0 = [0.0]*s; self.v0 = [0.0]*s
    def ix(self, x, y): return x + (self.n+2)*y
    def add_density(self, x, y, amount):
        self.d[self.ix(x, y)] += amount
    def add_velocity(self, x, y, vx, vy):
        self.u[self.ix(x, y)] += vx; self.v[self.ix(x, y)] += vy
    def _diffuse(self, b, x, x0, diff):
        n = self.n; a = self.dt * diff * n * n
        for _ in range(20):
            for j in range(1, n+1):
                for i in range(1, n+1):
                    x[self.ix(i,j)] = (x0[self.ix(i,j)] + a*(
                        x[self.ix(i-1,j)]+x[self.ix(i+1,j)]+
                        x[self.ix(i,j-1)]+x[self.ix(i,j+1)])) / (1+4*a)
    def _advect(self, b, d, d0, u, v):
        n = self.n; dt0 = self.dt * n
        for j in range(1, n+1):
            for i in range(1, n+1):
                x = i - dt0*u[self.ix(i,j)]; y = j - dt0*v[self.ix(i,j)]
                x = max(0.5, min(n+0.5, x)); y = max(0.5, min(n+0.5, y))
                i0, j0 = int(x), int(y); i1, j1 = i0+1, j0+1
                s1, s0 = x-i0, 1-(x-i0); t1, t0 = y-j0, 1-(y-j0)
                d[self.ix(i,j)] = (s0*(t0*d0[self.ix(i0,j0)]+t1*d0[self.ix(i0,j1)])+
                                   s1*(t0*d0[self.ix(i1,j0)]+t1*d0[self.ix(i1,j1)]))
    def step(self):
        self._diffuse(0, self.d0, self.d, self.diff)
        self._advect(0, self.d, self.d0, self.u, self.v)
    def render(self):
        chars = " ░▒▓█"
        lines = []
        for j in range(1, self.n+1):
            row = ""
            for i in range(1, self.n+1):
                v = min(1, max(0, self.d[self.ix(i, j)]))
                row += chars[min(len(chars)-1, int(v * len(chars)))]
            lines.append(row)
        return "\n".join(lines)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    f = Fluid(n)
    mid = n // 2
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            f.add_density(mid+dx, mid+dy, 2.0)
    f.add_velocity(mid, mid, 5.0, 3.0)
    for i in range(steps):
        os.system("clear" if os.name != "nt" else "cls")
        print(f"Fluid sim: step {i+1}/{steps}")
        print(f.render())
        f.step()
        if i < steps - 1:
            f.add_density(mid, n//4, 0.5)
            f.add_velocity(mid, n//4, 0.5, 1.0)
        time.sleep(0.1)
