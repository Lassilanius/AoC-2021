from pathlib import Path
import re

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input5.txt')]

def either(f, g):
    return lambda *x: f(*x) or g(*x)

def isCardinal(p):
    return p[0] == p[2] or p[1] == p[3]

def isOrdinal(p):
    return abs(p[0] - p[2]) == abs(p[1] - p[3])

def countOverlaps(lines):
    xMax = max(max(x1, x2) for x1, _, x2, _ in lines)
    yMax = max(max(y1, y2) for _, y1, _, y2 in lines)
    grid = [[0] * (xMax + 1) for _ in range(yMax + 1)]
    for x1, y1, x2, y2 in lines:
        dx = (x2 > x1) - (x2 < x1)
        dy = (y2 > y1) - (y2 < y1)
        if dx and dy:
            for k in range(abs(x1 - x2) + 1):
                grid[y1 + k * dy][x1 + k * dx] += 1
        elif dx:
            for k in range(x1, x2 + dx, dx):
                grid[y1][k] += 1
        else:
            for k in range(y1, y2 + dy, dy):
                grid[k][x1] += 1
    return sum(sum(x > 1 for x in row) for row in grid)

def main():
    for p in paths:
        with p.open('r') as f:
            lines  = [tuple(map(int, re.findall(r'\d+', x))) for x in f.readlines()]
            linesB = [*filter(either(isCardinal, isOrdinal), lines)]
            linesA = [*filter(isCardinal, linesB)]
            print(countOverlaps(linesA))
            print(countOverlaps(linesB))

if __name__ == '__main__':
    main()
