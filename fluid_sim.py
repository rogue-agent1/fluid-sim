import argparse, math

def make_grid(n): return [[0.0]*n for _ in range(n)]

def diffuse(grid, diff, dt, n):
    a = dt * diff * n * n
    new = [row[:] for row in grid]
    for _ in range(20):
        for i in range(1, n-1):
            for j in range(1, n-1):
                new[i][j] = (grid[i][j] + a * (new[i-1][j]+new[i+1][j]+new[i][j-1]+new[i][j+1])) / (1+4*a)
    return new

def advect(grid, vx, vy, dt, n):
    new = make_grid(n)
    for i in range(1, n-1):
        for j in range(1, n-1):
            x = i - dt * n * vx[i][j]
            y = j - dt * n * vy[i][j]
            x = max(0.5, min(n-1.5, x))
            y = max(0.5, min(n-1.5, y))
            i0, j0 = int(x), int(y)
            s1, s0 = x-i0, 1-(x-i0)
            t1, t0 = y-j0, 1-(y-j0)
            i1, j1 = min(i0+1, n-1), min(j0+1, n-1)
            new[i][j] = s0*(t0*grid[i0][j0]+t1*grid[i0][j1]) + s1*(t0*grid[i1][j0]+t1*grid[i1][j1])
    return new

def display(grid, n, chars=" ░▒▓█"):
    mx = max(max(abs(v) for v in row) for row in grid) or 1
    for row in grid:
        print("".join(chars[min(int(abs(v)/mx*(len(chars)-1)), len(chars)-1)] for v in row))

def main():
    p = argparse.ArgumentParser(description="2D fluid simulation")
    p.add_argument("-n", "--size", type=int, default=30)
    p.add_argument("-s", "--steps", type=int, default=50)
    p.add_argument("--diff", type=float, default=0.0001)
    args = p.parse_args()
    n = args.size
    density = make_grid(n)
    vx, vy = make_grid(n), make_grid(n)
    # Add initial source
    for i in range(n//3, 2*n//3):
        density[n//2][i] = 1.0
        vy[n//2][i] = 0.5
        vx[n//3][i] = 0.3
    dt = 0.1
    for step in range(args.steps):
        density = diffuse(density, args.diff, dt, n)
        density = advect(density, vx, vy, dt, n)
        vx = diffuse(vx, args.diff, dt, n)
        vy = diffuse(vy, args.diff, dt, n)
        if step % 10 == 0:
            print(f"--- Step {step} ---")
            display(density, n)

if __name__ == "__main__":
    main()
