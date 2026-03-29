#!/usr/bin/env python3
"""Simplified 2D fluid simulation using Jos Stam's stable fluids."""
import sys

class FluidSim:
    def __init__(self, n=20, diff=0.0001, visc=0.0001, dt=0.1):
        self.n, self.diff, self.visc, self.dt = n, diff, visc, dt
        s = (n+2)**2
        self.u = [0.0]*s; self.v = [0.0]*s; self.dens = [0.0]*s
    def _ix(self, x, y): return x + (self.n+2)*y
    def _diffuse(self, x, x0, diff):
        a = self.dt * diff * self.n * self.n; n = self.n
        for _ in range(20):
            for j in range(1, n+1):
                for i in range(1, n+1):
                    idx = self._ix(i,j)
                    x[idx] = (x0[idx]+a*(x[self._ix(i-1,j)]+x[self._ix(i+1,j)]+x[self._ix(i,j-1)]+x[self._ix(i,j+1)]))/(1+4*a)
    def add_source(self, x, y, amount):
        self.dens[self._ix(x,y)] += amount
    def add_velocity(self, x, y, vx, vy):
        self.u[self._ix(x,y)] += vx; self.v[self._ix(x,y)] += vy
    def step(self):
        u0 = self.u[:]; v0 = self.v[:]; d0 = self.dens[:]
        self._diffuse(self.u, u0, self.visc)
        self._diffuse(self.v, v0, self.visc)
        self._diffuse(self.dens, d0, self.diff)
    def display(self):
        chars = " ·░▒▓█"; n = self.n
        for j in range(1, n+1):
            row = ""
            for i in range(1, n+1):
                d = min(self.dens[self._ix(i,j)], 5)
                row += chars[int(d)]
            print(row)

def main():
    sim = FluidSim(20)
    sim.add_source(10, 10, 5); sim.add_velocity(10, 10, 2, 1)
    sim.add_source(10, 11, 5); sim.add_source(11, 10, 5)
    for _ in range(50): sim.step()
    print("Fluid density after 50 steps:")
    sim.display()

if __name__ == "__main__": main()
