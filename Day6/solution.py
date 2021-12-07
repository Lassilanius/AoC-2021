from pathlib import Path

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input6.txt')]

cycle, offset = 7, 2

def countLanternfish(initial, days):
    newBorns = [0] * (days + 1)
    for x in initial:
        for i in range(x + 1, days + 1, cycle):
            newBorns[i] += 1
    for i, x in enumerate(newBorns, cycle + offset):
        for j in range(i, days + 1, cycle):
            newBorns[j] += x
    return sum(newBorns) + len(initial)

def main():
    for p in paths:
        with p.open('r') as f:
            data = list(map(int, f.read().split(',')))
            print(countLanternfish(data, 80))
            print(countLanternfish(data, 256))

if __name__ == '__main__':
    main()
