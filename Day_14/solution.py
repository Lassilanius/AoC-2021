from pathlib import Path
from collections import defaultdict

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

def solve(seq, rules, iterations):
    pairCount   = defaultdict(int)
    letterCount = defaultdict(int)
    for i, x in enumerate(seq):
        pairCount[seq[i: i + 2]] += 1
        letterCount[x] += 1 
    del pairCount[seq[-1]]
    for _ in range(iterations):
        npc = defaultdict(int)
        for k, v in pairCount.items():
            if k in rules:
                npc[k[0] + rules[k]]  += v
                npc[rules[k] + k[1]]  += v
                letterCount[rules[k]] += v
        pairCount = npc
    return max(letterCount.values()) - min(letterCount.values())

def main():
    for p in paths:
        with p.open('r') as f:
            data  = f.read().split('\n')
            seq   = data[0]
            rules = dict(r.split(' -> ') for r in data[2:])
            print(solve(seq, rules, 10))
            print(solve(seq, rules, 40))

if __name__ == '__main__':
    main()
