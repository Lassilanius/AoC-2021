from pathlib import Path
from operator import or_

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input.txt')]

class FoldableGrid:

    def __init__(self, grid):
        self.grid = grid

    def __str__(self):
        return '\n'.join(''.join('#' if x else ' ' for x in row) for row in self.grid)

    def fold(self, fold):
        return self.foldN([fold])

    def foldN(self, folds):
        grid = self.grid
        for f in folds:
            axis, idx = f.split('=')
            i = int(idx)
            if axis == 'y':
                grid = tuple(tuple(map(or_, a, b)) for a, b in zip(grid[:i], grid[:i:-1]))
            else:
                grid = tuple(tuple(map(or_, a, b)) for a, b in zip((r[:i] for r in grid), (r[:i:-1] for r in grid)))
        return FoldableGrid(grid)

    def sumGrid(self):
        return sum(sum(row) for row in self.grid)


def main():
    for p in paths:
        with p.open('r') as f:
            data = f.read().split('\n')
            points, folds = set(), []
            i = 0
            while data[i]:
                points.add(tuple(map(int, data[i].split(','))))
                i += 1
            i += 1
            while i < len(data):
                folds.append(data[i].replace('fold along ', ''))
                i += 1
            numCols = max(x for x, _ in points) + 1
            numRows = max(y for _, y in points) + 1
            grid    = tuple(tuple(int((i, j) in points) for i in range(numCols)) for j in range(numRows))
            foldableGrid = FoldableGrid(grid)
            print(foldableGrid.fold(folds[0]).sumGrid())
            print(foldableGrid.foldN(folds))

if __name__ == '__main__':
    main()
