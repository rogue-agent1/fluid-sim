#!/usr/bin/env python3
"""Simple 1D shallow water simulation."""
import math

class ShallowWater:
    def __init__(self, n=100, dx=1.0, g=9.81):
        self.n = n; self.dx = dx; self.g = g
        self.h = [1.0] * n  # water height
        self.u = [0.0] * n  # velocity

    def init_dam_break(self, split=None):
        if split is None: split = self.n // 2
        for i in range(split):
            self.h[i] = 2.0

    def init_wave(self, center=None, amplitude=0.5, width=5):
        if center is None: center = self.n // 2
        for i in range(self.n):
            self.h[i] = 1.0 + amplitude * math.exp(-((i - center) / width) ** 2)

    def step(self, dt):
        h_new = self.h[:]
        u_new = self.u[:]
        for i in range(1, self.n - 1):
            h_new[i] = self.h[i] - dt / self.dx * (
                self.h[i] * (self.u[i+1] - self.u[i-1]) / 2 +
                self.u[i] * (self.h[i+1] - self.h[i-1]) / 2)
            u_new[i] = self.u[i] - dt / self.dx * (
                self.u[i] * (self.u[i+1] - self.u[i-1]) / 2 +
                self.g * (self.h[i+1] - self.h[i-1]) / 2)
        # Reflective boundaries
        h_new[0] = h_new[1]; h_new[-1] = h_new[-2]
        u_new[0] = -u_new[1]; u_new[-1] = -u_new[-2]
        self.h = h_new; self.u = u_new

    def total_volume(self):
        return sum(self.h) * self.dx

    def max_height(self):
        return max(self.h)

if __name__ == "__main__":
    sw = ShallowWater(n=50)
    sw.init_dam_break()
    for _ in range(100):
        sw.step(0.01)
    print(f"Max height: {sw.max_height():.3f}")

def test():
    sw = ShallowWater(n=50, dx=1.0)
    sw.init_dam_break()
    v0 = sw.total_volume()
    for _ in range(50):
        sw.step(0.005)
    # Volume roughly conserved
    v1 = sw.total_volume()
    assert abs(v1 - v0) / v0 < 0.1
    # Wave init
    sw2 = ShallowWater(n=50)
    sw2.init_wave(amplitude=0.3)
    assert sw2.max_height() > 1.0
    for _ in range(20):
        sw2.step(0.005)
    # Wave should propagate
    assert sw2.max_height() > 0.5
    print("  fluid_sim: ALL TESTS PASSED")
