from fluid_sim import FluidGrid
g = FluidGrid(20, 20)
g.add_source(10, 10, 5, 3)
assert g.density[10][10] > 0
for _ in range(10): g.step(0.1, 0.5)
a = g.to_ascii()
assert len(a) > 0
print("Fluid sim tests passed")