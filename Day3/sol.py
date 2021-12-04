from pathlib import Path
from itertools import islice
from operator import ge, lt

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input3.txt')]

def solveA(data):
    half    = len(data) // 2
    gamma   = int(''.join('0' if r.count('0') > half else '1' for r in zip(*data)), 2)
    epsilon = gamma ^ int('1' * len(data[0]), 2)
    return gamma * epsilon

def solveB(data):
    res = 1
    for cmp in ge, lt:
        i, arr = 0, data[:]
        while len(arr) > 1:
            bit = '1' if cmp(next(islice(zip(*arr), i, None)).count('1'), len(arr) / 2) else '0'
            arr = [x for x in arr if x[i] == bit]
            i  += 1
        res *= int(arr[0], 2)
    return res

def main():
    for p in paths:
        with p.open('r') as f:
            data = list(map(str.strip, f.readlines()))
            print(solveA(data))
            print(solveB(data))

if __name__ == '__main__':
    main()
