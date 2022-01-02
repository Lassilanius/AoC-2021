from pathlib import Path

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

class TrenchMap:

    def __init__(self, grid, bitstr):
        self.bitstr  = bitstr
        self.grid    = grid
        self.numRows = len(grid)
        self.numCols = len(grid[0])

    def __str__(self):
        return '\n'.join(self.grid)

    def countLitPixels(self):
        return sum(row.count('#') for row in self.grid)

    def evolve(self, iterations = 1):
        bitstr  = self.bitstr
        grid    = self.grid
        numRows = self.numRows
        numCols = self.numCols
        for _ in range(iterations):
            pad  = '#' if grid[0][0] != bitstr[0] else '.'
            res  = [pad * (numCols + 2)] * 2
            for i in range(1, numRows - 1):
                row = pad + pad
                for j in range(1, numCols - 1):
                    b = grid[i - 1][j - 1: j + 2] + grid[i][j - 1: j + 2] + grid[i + 1][j - 1: j + 2]
                    n = int(b.replace('#', '1').replace('.', '0'), 2)
                    row += bitstr[n]
                row += pad + pad
                res.append(row)
            res.extend(res[:2])
            grid = res
            numRows, numCols = len(grid), len(grid[0])
        return TrenchMap(res, bitstr)


def main():
    for p in paths:
        with p.open('r') as f:
            data = f.read().split('\n')
            bitstr = ''
            i = 0
            while data[i]:
                bitstr += data[i]
                i += 1
            grid = ['.' * (4 + len(data[i + 1]))] * 2
            for row in data[i + 1:]:
                grid.append('..' + row + '..')
            grid.extend(grid[:2])
            trenchMap = TrenchMap(grid, bitstr)
            print(trenchMap.evolve(2).countLitPixels())
            print(trenchMap.evolve(50).countLitPixels())

if __name__ == '__main__':
    main()
