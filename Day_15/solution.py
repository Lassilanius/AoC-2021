from pathlib import Path
from itertools import chain
from heapq import *

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

class Pathfinder:

    directions = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, grid):
        self.grid    = grid
        self.numRows = len(grid)
        self.numCols = len(grid[0])

    def isOnGrid(self, i, j):
        return 0 <= i < self.numRows and 0 <= j < self.numCols

    def getNeighbours(self, i, j):
        return [(i + di, j + dj) for di, dj in Pathfinder.directions if self.isOnGrid(i + di, j + dj)]

    def sumMinRiskPath(self):
        start, end = (0, 0), (self.numRows - 1, self.numCols - 1)
        dist = [[float('inf')] * self.numCols for _ in range(self.numRows)]
        dist[0][0] = 0

        grid = self.grid
        pq   = [(0, start)]
        pred = {start: None}

        while pq:
            d, (i, j) = heappop(pq)
            if (i, j) == end:
                break
            for k, l in self.getNeighbours(i, j):
                if dist[k][l] > d + grid[k][l]:
                    dist[k][l]   = d + grid[k][l]
                    pred[(k, l)] = (i, j)
                    heappush(pq, (dist[k][l], (k, l)))

        pos, riskSum = end, 0
        while pred[pos]:
            i, j = pos
            riskSum += grid[i][j]
            pos = pred[pos]
        return riskSum


def scaledRow(row, factor):
    return [(x - 1 + factor) % 9 + 1 for x in row]

def scaledGrid(grid, factor):
    return [[*chain.from_iterable(scaledRow(row, i + j) for j in range(factor))]
            for i in range(factor) for row in grid]

def main():
    for p in paths:
        with p.open('r') as f:
            grid = [[*map(int, x)] for x in f.read().split('\n')]
            print(Pathfinder(grid).sumMinRiskPath())
            print(Pathfinder(scaledGrid(grid, 5)).sumMinRiskPath())

if __name__ == '__main__':
    main()
