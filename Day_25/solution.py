from pathlib import Path

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

def solve(grid):
    M, N = len(grid), len(grid[0])
    hs = {(i, j) for i, row in enumerate(grid) for j, x in enumerate(row) if x == '>'}
    vs = {(i, j) for i, row in enumerate(grid) for j, x in enumerate(row) if x == 'v'}
    it = 0

    while True:
        it += 1
        toMove = []

        for i, j in hs:
            k = (j + 1) % N
            if grid[i][k] == '.':
                toMove.append((i, j, k))

        changed = bool(toMove)
        for i, j, k in toMove:
            grid[i][j] = '.'
            grid[i][k] = '>'
            hs.remove((i, j))
            hs.add((i, k))

        toMove = []
        for i, j in vs:
            k = (i + 1) % M
            if grid[k][j] == '.':
                toMove.append((i, j, k))

        changed = changed or bool(toMove)
        for i, j, k in toMove:
            grid[i][j] = '.'
            grid[k][j] = 'v'
            vs.remove((i, j))
            vs.add((k, j))

        if not changed:
            return it

def main():
    for p in paths:
        with p.open('r') as f:
            grid = [*map(list, f.read().split('\n'))]
            print(solve(grid))

if __name__ == '__main__':
    main()
