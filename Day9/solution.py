from pathlib import Path
from math import prod

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input.txt')]

class Heightmap:

    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, data):
        self.grid    = tuple(tuple(map(int, line)) for line in data.split('\n'))
        self.numRows = len(self.grid)
        self.numCols = len(self.grid[0])

    def isOnGrid(self, i, j):
        return 0 <= i < self.numRows and 0 <= j < self.numCols

    def getNeighbours(self, i, j):
        return [(i + di, j + dj) for di, dj in Heightmap.directions if self.isOnGrid(i + di, j + dj)]

    def sumRiskLevels(self):
        return sum(self.grid[i][j] + 1 for i, row in enumerate(self.grid) for j, height in enumerate(row)
                   if all(self.grid[k][l] > height for k, l in self.getNeighbours(i, j)))

    def getSizesOfBasins(self):
        visited       = set()
        sizesOfBasins = []

        def dfs(i, j):
            if (i, j) in visited or self.grid[i][j] == 9:
                return
            visited.add((i, j))
            sizesOfBasins[-1] += 1
            for k, l in self.getNeighbours(i, j):
                dfs(k, l)

        for i, row in enumerate(self.grid):
            for j, height in enumerate(row):
                if (i, j) not in visited and height != 9:
                    sizesOfBasins.append(0)
                    dfs(i, j)

        return sizesOfBasins

    def productOfThreeLargestBasins(self):
        return prod(sorted(self.getSizesOfBasins())[-3:])

def main():
    for p in paths:
        with p.open('r') as f:
            hmap = Heightmap(f.read())
            print(hmap.sumRiskLevels())
            print(hmap.productOfThreeLargestBasins())

if __name__ == '__main__':
    main()
