from pathlib import Path

def solveA(data):
    return sum(int(val) for cmd, val in map(str.split, data) if cmd == 'forward') * \
           sum(int(val) * ((cmd == 'down') - (cmd == 'up')) for cmd, val in map(str.split, data))

def solveB(data):
    x, y, aim = 0, 0, 0
    for cmd, val in map(str.split, data):
        v = int(val)
        if   cmd == 'forward': x, y = x + v, y + v * aim
        elif cmd == 'down':    aim += v
        elif cmd == 'up':      aim -= v
    return x * y

def main():
    sampleData = 'forward 5,down 5,forward 8,up 3,down 8,forward 2'.split(',')
    print(solveA(sampleData))
    print(solveB(sampleData))

    p = Path(__file__).with_name('input2.txt')
    with p.open('r') as f:
        data = f.readlines()
        print(solveA(data))
        print(solveB(data))

if __name__ == '__main__':
    main()
