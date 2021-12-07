from pathlib import Path
from statistics import median, mean
from math import floor

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input7.txt')]

def solveA(data):
    m = floor(median(data))
    return min(sum(abs(x - k) for x in data) for k in (m, m + 1))

def solveB(data):
    m = floor(mean(data))
    return min(sum((d := abs(x - k)) * (d + 1) // 2 for x in data) for k in (m, m + 1))

def main():
    for p in paths:
        with p.open('r') as f:
            data = list(map(int, f.read().split(',')))
            print(solveA(data))
            print(solveB(data))

if __name__ == '__main__':
    main()
