from pathlib import Path
from itertools import accumulate, chain, groupby, islice
import re
import numpy as np
import time

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

def uncompressedSum(arr, xs):
    indices = [*accumulate(len(tuple(g)) for _, g in groupby(chain([0], arr)))]
    return sum(arr[i - 1] * (xs[j - 2] - xs[i - 1] + 1) for i, j in zip(indices, islice(indices, 1, None)))

def bruteForce(instructions):
    ''' Brute force with index compression. '''

    xs = sorted({x for _, t in instructions for x in (t[0] - 1, t[0], t[0] + 1, t[1] - 1, t[1], t[1] + 1)})[1:-1]
    ys = sorted({y for _, t in instructions for y in (t[2] - 1, t[2], t[2] + 1, t[3] - 1, t[3], t[3] + 1)})[1:-1]
    zs = sorted({z for _, t in instructions for z in (t[4] - 1, t[4], t[4] + 1, t[5] - 1, t[5], t[5] + 1)})[1:-1]

    dx = {x: i for i, x in enumerate(xs)}
    dy = {y: i for i, y in enumerate(ys)}
    dz = {z: i for i, z in enumerate(zs)}
    
    M, N, K = len(xs), len(ys), len(zs)
    grid = np.zeros((M, N, K), np.int8)
    for cmd, (x0, x1, y0, y1, z0, z1) in instructions:
        xa, xb = dx[x0], dx[x1] + 1
        ya, yb = dy[y0], dy[y1] + 1
        za, zb = dz[z0], dz[z1] + 1
        ws = np.ones(zb - za) if cmd == 'on' else np.zeros(zb - za)
        grid[xa: xb, ya: yb, za: zb] = ws

    arr = []
    for x in range(M):
        xarr = [uncompressedSum(grid[x][y].tolist(), zs) for y in range(N)]
        arr.append(uncompressedSum(xarr, ys))
    return uncompressedSum(arr, xs)

def main():
    for p in paths:
        with p.open('r') as f:
            t0 = time.time()
            instructions = [(x[:3].strip(), tuple(map(int, re.findall(r'\-?\d+', x)))) for x in f.read().split('\n')]
            smallRegion  = [(cmd, coords) for cmd, coords in instructions if all(-50 <= x <= 50 for x in coords)]
            print(bruteForce(smallRegion))
            print(bruteForce(instructions))
            print(f'Run time in seconds: {time.time() - t0}')

if __name__ == '__main__':
    main()
