from pathlib import Path
from statistics import median

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input.txt')]
illegalScoreTable = (3, 57, 1197, 25137)

def solve(data):
    scoreOfIllegals = 0
    complementaries = []

    lp, rp = '([{<', ')]}>'
    mirror = dict(zip(rp + lp, lp + rp))

    for line in data:
        stack, isLegal = [''], True
        for tok in line:
            if tok in lp:
                stack.append(tok)
            else:
                if stack[-1] == mirror[tok]:
                    stack.pop()
                else:
                    scoreOfIllegals += illegalScoreTable[rp.index(tok)]
                    isLegal = False
                    break

        if isLegal:
            complementaries.append(''.join(mirror[x] for x in stack[-1: 0: -1]))

    scores = [0] * len(complementaries)
    for i, ps in enumerate(complementaries):
        for p in ps:
            scores[i] = scores[i] * 5 + rp.index(p) + 1

    return scoreOfIllegals, median(scores)

def main():
    for p in paths:
        with p.open('r') as f:
            print(solve(f.read().split('\n')))

if __name__ == '__main__':
    main()
