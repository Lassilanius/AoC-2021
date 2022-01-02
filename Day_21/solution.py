from itertools import cycle
from collections import Counter

STARTING_POSITIONS = [(4, 8), (7, 8)]

class DeterministicDice:

    def __init__(self, sides = 100):
        self.sides = sides

    def __iter__(self):
        yield from cycle(range(1, self.sides + 1))

def solveA(posA, posB):
    dice      = DeterministicDice()
    roll      = iter(dice)
    pos       = [posA, posB]
    scores    = [0, 0]
    nrOfRolls = 0
    while True:
        for i in 0, 1:
            pos[i]     = (sum(next(roll) for _ in range(3)) + pos[i] - 1) % 10 + 1
            nrOfRolls += 3
            scores[i] += pos[i]
            if scores[i] >= 1000:
                return min(scores) * nrOfRolls

def solveB(posA, posB):
    wins     = 0
    limit    = 21
    size     = 10
    M, N     = limit + size, size
    outcomes = (1, 2, 3)
    rollFreq = Counter(x + y + z
                       for x in outcomes
                       for y in outcomes
                       for z in outcomes).most_common()

    dpTables = [ [[0] * N for _ in range(M)], [[0] * N for _ in range(M)] ]
    dpTables[0][0][posA - 1] = 1
    dpTables[1][0][posB - 1] = 1

    while True:
        for turn in 0, 1:
            dp = [[0] * N for _ in range(M)]
            changed = False
            for i in range(M):
                for j in range(N):
                    s, p, m = i, j, dpTables[turn][i][j]
                    if m > 0 and s < limit:
                        for x, c in rollFreq:
                            z = (p + x) % size
                            dp[s + z + 1][z] += m * c
                            changed = True
            if turn == 0:
                bLose = sum(dpTables[1][i][j] for i in range(limit) for j in range(N))
                aWins = sum(dp[i][j] for i in range(limit, M) for j in range(N)) * bLose
                wins += aWins
            if changed:
                dpTables[turn] = dp
            else:
                return wins

def main():
    for posA, posB in STARTING_POSITIONS:
        print(solveA(posA, posB))
        print(solveB(posA, posB))

if __name__ == '__main__':
    main()
