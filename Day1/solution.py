from pathlib import Path
from itertools import islice
from operator import lt

def summedWindows(data, windowSize):
    return [sum(data[i: i + windowSize]) for i in range(len(data) - windowSize + 1)]

def countIncrements(data):
    return sum(map(lt, data, islice(data, 1, None)))

def main():
    sampleData = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    print(countIncrements(sampleData))
    print(countIncrements(summedWindows(sampleData, 3)))

    p = Path(__file__).with_name('input1.txt')
    with p.open('r') as f:
        data = list(map(int, f.readlines()))
        print(countIncrements(data))
        print(countIncrements(summedWindows(data, 3)))

if __name__ == '__main__':
    main()
