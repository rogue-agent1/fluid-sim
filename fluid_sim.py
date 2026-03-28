#!/usr/bin/env python3
"""1D fluid diffusion simulation with ASCII visualization."""
import sys, time
def simulate(n=60, steps=100, diff=0.2):
    u=[0.0]*n; u[n//2]=10.0
    for step in range(steps):
        new=[0.0]*n
        for i in range(1,n-1):
            new[i]=u[i]+diff*(u[i-1]-2*u[i]+u[i+1])
        new[0]=new[1]; new[-1]=new[-2]; u=new
        h=10; mx=max(max(u),0.01)
        print(f"\033[2J\033[HStep {step}, max={mx:.3f}")
        for row in range(h,-1,-1):
            threshold=row/h*mx
            print("".join("█" if u[i]>=threshold else " " for i in range(n)))
        time.sleep(0.05)
def cli():
    simulate(steps=int(sys.argv[1]) if len(sys.argv)>1 else 80)
if __name__=="__main__": cli()
