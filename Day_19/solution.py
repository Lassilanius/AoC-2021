from pathlib import Path
from itertools import islice
from collections import deque
from functools import partial
from operator import mul
from math import pi, cos, sin
from time import time

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

def genRotations(angles):
    for a in angles:
        for b in angles:
            for c in angles:
                yield (
                       (cos(a) * cos(b), cos(a) * sin(b) * sin(c) - sin(a) * cos(c), cos(a) * sin(b) * cos(c) + sin(a) * sin(c)),
                       (sin(a) * cos(b), sin(a) * sin(b) * sin(c) + cos(a) * cos(c), sin(a) * sin(b) * cos(c) - cos(a) * sin(c)),
                       (-sin(b), cos(b) * sin(c), cos(b) * cos(c))
                      )

def rotate(rotMat, vec):
    return tuple(sum(map(mul, row, vec)) for row in rotMat)

ANGLES    = (0, pi / 2, pi, -pi / 2)
ROTATIONS = set(tuple(tuple(map(round, row)) for row in mat) for mat in genRotations(ANGLES))
ROTFUNCS  = tuple(partial(rotate, rot) for rot in ROTATIONS)

def subtract(p, q):
    return p[0] - q[0], p[1] - q[1], p[2] - q[2]

def shifted(points, shift):
    return {subtract(p, shift) for p in points}

def manhattanDist(p, q):
    return sum(map(abs, subtract(p, q)))

def allPossibleShifts(ps, qs):
    return {subtract(p, q) for p in ps for q in qs}

def countOverlaps(ps, qs, shift):
    return sum(subtract(q, shift) in ps for q in qs)

def solve(scanners, overlapsToMatch = 12):
    beacons          = scanners[0]
    posOfScanners    = [None] * len(scanners)
    posOfScanners[0] = (0, 0, 0)
    processed        = set()
    todo             = deque([(0, scanners[0])])

    def rotateShiftAndMatch(ps, qs, i):
        nonlocal beacons
        for rotFunc in ROTFUNCS:
            rs = set(map(rotFunc, qs))
            for shift in allPossibleShifts(rs, ps):
                overlaps = countOverlaps(ps, rs, shift)
                if overlaps >= overlapsToMatch:
                    scanners[i]       = shifted(rs, shift)
                    beacons          |= scanners[i]
                    posOfScanners[i]  = tuple(-x for x in shift)
                    todo.append((i, scanners[i]))
                    return

    while todo:
        i, ps = todo.popleft()
        if i in processed:
            continue
        processed.add(i)
        for j, qs in enumerate(scanners):
            if not posOfScanners[j]:
                rotateShiftAndMatch(ps, qs, j)

    print(f'Number of beacons = {len(beacons)}')
    maxManDist = max(manhattanDist(x, y)
                     for i, x in enumerate(posOfScanners)
                     for y in islice(posOfScanners, i + 1, None))
    print(f'Largest manhattan distance = {maxManDist}')

def main():
    for p in paths:
        with p.open('r') as f:
            t0 = time()
            scanners = []
            for line in f.read().split('\n'):
                if line[:3] == '---':
                    scanners.append(set())
                elif line:
                    scanners[-1].add(tuple(map(int, line.split(','))))

            solve(scanners)
            print(f'Run time in seconds: {time() - t0}')

if __name__ == '__main__':
    main()
