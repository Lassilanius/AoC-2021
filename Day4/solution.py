from pathlib import Path

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input4.txt')]

class BingoBoard:

    def __init__(self, board):
        self.board = board

    def __str__(self):
        return '\n'.join(', '.join(str(x).rjust(2, ' ') for x in row) for row in self.board)

    def isWon(self):
        return any(all(x == -1 for x in row) for row in self.board) or \
               any(all(x == -1 for x in col) for col in zip(*self.board))

    def getScore(self):
        return sum(x for row in self.board for x in row if x > 0)

    def crossOut(self, n):
        return BingoBoard(tuple(tuple(-(x == n) or x for x in row) for row in self.board))


def solveA(nums, boards):
    for n in nums:
        boards = [b.crossOut(n) for b in boards]
        for b in boards:
            if b.isWon():
                return b.getScore() * n

def solveB(nums, boards):
    for i, n in enumerate(nums):
        boards = [nb for b in boards if not (nb := b.crossOut(n)).isWon()]
        if len(boards) == 1:
            return solveA(nums[i + 1:], boards)

def main():
    for p in paths:
        with p.open('r') as f:
            lines = f.read().split('\n') + ['']
            nums  = list(map(int, lines[0].split(',')))
            b, boards = [], []
            for l in lines[1:]:
                if l:
                    b.append(tuple(map(int, l.split())))
                elif b:
                    boards.append(BingoBoard(tuple(b)))
                    b = []

            print(solveA(nums, boards))
            print(solveB(nums, boards))

if __name__ == '__main__':
    main()
