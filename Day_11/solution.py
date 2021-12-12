from pathlib import Path

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input.txt')]

class FlashGrid:

    directions = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))

    def __init__(self, data):
        self.grid    = [list(map(int, line)) for line in data.split('\n')]
        self.numRows = len(self.grid)
        self.numCols = len(self.grid[0])

    def isOnGrid(self, i, j):
        return 0 <= i < self.numRows and 0 <= j < self.numCols

    def getNeighbours(self, i, j):
        return [(i + di, j + dj) for di, dj in FlashGrid.directions if self.isOnGrid(i + di, j + dj)]

    def flashesFromOneIter(self, grid): # Mutates grid
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                grid[i][j] = 1 + x * (x < 10)

        used = set()
        flashes, somethingFlashed = 0, True
        while somethingFlashed:
            somethingFlashed = False
            for i in range(self.numRows):
                for j in range(self.numCols):
                    if grid[i][j] > 9 and (i, j) not in used:
                        somethingFlashed = True
                        flashes += 1
                        used.add((i, j))
                        for ii, jj in self.getNeighbours(i, j):
                            grid[ii][jj] += 1
        return flashes

    def countFlashes(self, iterations):
        mutableGrid = [row[:] for row in self.grid]
        return sum(self.flashesFromOneIter(mutableGrid) for _ in range(iterations))

    def firstSynchronizingFlash(self):
        it, maxIterations = 0, 10000
        mutableGrid = [row[:] for row in self.grid]
        while it < maxIterations:
            it += 1
            if self.flashesFromOneIter(mutableGrid) == self.numRows * self.numCols:
                return it

def main():
    for p in paths:
        with p.open('r') as f:
            flashGrid = FlashGrid(f.read())
            print(flashGrid.countFlashes(100))
            print(flashGrid.firstSynchronizingFlash())

if __name__ == '__main__':
    main()
