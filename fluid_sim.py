#!/usr/bin/env python3
"""fluid_sim - 1D Euler fluid sim."""
import sys,argparse,json,math
def simulate(n=100,steps=200,dt=0.01):
    rho=[1.0]*n;vel=[0.0]*n;pressure=[1.0]*n
    for i in range(n//3,2*n//3):rho[i]=2.0;pressure[i]=2.0
    snapshots=[]
    for step in range(steps):
        new_rho=rho[:];new_vel=vel[:];new_p=pressure[:]
        for i in range(1,n-1):
            new_rho[i]=rho[i]-dt*(rho[i]*(vel[i+1]-vel[i-1])/(2*dt*10)+vel[i]*(rho[i+1]-rho[i-1])/(2*dt*10))
            new_vel[i]=vel[i]-dt*(vel[i]*(vel[i+1]-vel[i-1])/(2*dt*10)+(pressure[i+1]-pressure[i-1])/(2*dt*10*rho[i]))
            new_p[i]=new_rho[i]
        rho,vel,pressure=new_rho,new_vel,new_p
        if step%(steps//5)==0:snapshots.append({"step":step,"density":[round(r,3) for r in rho[::5]]})
    return snapshots
def main():
    p=argparse.ArgumentParser(description="Fluid sim")
    p.add_argument("--points",type=int,default=100);p.add_argument("--steps",type=int,default=100)
    args=p.parse_args()
    snaps=simulate(args.points,args.steps)
    print(json.dumps({"points":args.points,"steps":args.steps,"snapshots":snaps},indent=2))
if __name__=="__main__":main()
