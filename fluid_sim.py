#!/usr/bin/env python3
"""Simple 2D fluid simulation (Lattice Boltzmann Method lite)."""
import math
def diffuse(grid,nx,ny,diff,dt):
    a=dt*diff*nx*ny;new=[[0.0]*ny for _ in range(nx)]
    for _ in range(20):
        for i in range(1,nx-1):
            for j in range(1,ny-1):
                new[i][j]=(grid[i][j]+a*(new[i-1][j]+new[i+1][j]+new[i][j-1]+new[i][j+1]))/(1+4*a)
    return new
def advect(grid,vx,vy,nx,ny,dt):
    new=[[0.0]*ny for _ in range(nx)]
    for i in range(1,nx-1):
        for j in range(1,ny-1):
            x=i-dt*nx*vx[i][j];y=j-dt*ny*vy[i][j]
            x=max(0.5,min(nx-1.5,x));y=max(0.5,min(ny-1.5,y))
            i0=int(x);j0=int(y);s1=x-i0;s0=1-s1;t1=y-j0;t0=1-t1
            new[i][j]=s0*(t0*grid[i0][j0]+t1*grid[i0][min(j0+1,ny-1)])+s1*(t0*grid[min(i0+1,nx-1)][j0]+t1*grid[min(i0+1,nx-1)][min(j0+1,ny-1)])
    return new
if __name__=="__main__":
    nx=ny=32;density=[[0.0]*ny for _ in range(nx)]
    for i in range(12,20):
        for j in range(12,20): density[i][j]=1.0
    density=diffuse(density,nx,ny,0.1,0.1)
    total=sum(sum(row) for row in density)
    print(f"Fluid sim: {nx}x{ny} grid, total density={total:.2f}")
    print("Fluid sim OK")
