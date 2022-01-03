from pathlib import Path
from collections import defaultdict
import time

path = Path(__file__).with_name('input.txt')

def interpret(instructions, inp, z = 0):
    ''' For validation. '''

    mem = {'w': 0, 'x': 0, 'y': 0, 'z': z}
    for command in instructions:
        match command.split():
            case ['inp', a]:
                mem[a] = int(inp.pop())

            case ['add', a, ('w' | 'x' | 'y' | 'z') as b]:
                mem[a] += mem[b]

            case ['add', a, b]:
                mem[a] += int(b)

            case ['mul', a, ('w' | 'x' | 'y' | 'z') as b]:
                mem[a] *= mem[b]

            case ['mul', a, b]:
                mem[a] *= int(b)

            case ['div', a, ('w' | 'x' | 'y' | 'z') as b]:
                if mem[b] == 0:
                    raise ValueError
                mem[a] = int(mem[a] / mem[b])

            case ['div', a, b]:
                if int(b) == 0:
                    raise ValueError
                mem[a] = int(mem[a] / int(b))

            case ['mod', a, ('w' | 'x' | 'y' | 'z') as b]:
                if mem[a] < 0 or mem[b] <= 0:
                    raise ValueError
                mem[a] %= mem[b]

            case ['mod', a, b]:
                if mem[a] < 0 or int(b) <= 0:
                    raise ValueError
                mem[a] %= int(b)

            case ['eql', a, ('w' | 'x' | 'y' | 'z') as b]:
                mem[a] = int(mem[a] == mem[b])

            case ['eql', a, b]:
                mem[a] = int(mem[a] == int(b))
    return mem

def reducedInterpreter(w, z, p, q, r):
    if z % 26 + q != w:
        return z // p * 26 + w + r
    return z // p

def main():
    with Path(__file__).with_name('input.txt').open('r') as f:

        t0  = time.time()
        inp = f.read().split('\n')

        params = []
        for i, cmd in enumerate(inp):
            if i % 18 in (4, 5, 15): # These commands changes parameters
                _, _, p = cmd.split()
                params.append(int(p))
        params = [tuple(params[i: i + 3]) for i in range(0, len(params), 3)]

        # For each instruction, map the resulting z value (t) to the w, z parameters used as input
        zmap = [defaultdict(lambda: defaultdict(list)) for _ in range(len(params))]
        for i, (p, q, r) in enumerate(params):
            zs = zmap[i - 1] if i > 0 else [0]
            for w in range(1, 10):
                for z in zs:
                    t = reducedInterpreter(w, z, p, q, r)
                    zmap[i][t][w].append(z)

        def search(t = 0, i = 1, s = ''):
            if len(s) == 14:
                yield int(s)
                return
            if t in zmap[-i]:
                for w, zs in zmap[-i][t].items():
                    for z in zs:
                        yield from search(z, i + 1, str(w) + s)

        modelNumbers = list(search())
        maxModelNr   = max(modelNumbers)
        minModelNr   = min(modelNumbers)

        assert interpret(inp, [int(x) for x in str(maxModelNr)[::-1]])['z'] == 0
        assert interpret(inp, [int(x) for x in str(minModelNr)[::-1]])['z'] == 0

        print(f'number of model numbers = {len(modelNumbers)}')
        print(f'max model number = {maxModelNr}')
        print(f'min model number = {minModelNr}')
        print(f'Run time in seconds: {time.time() - t0}')

if __name__ == '__main__':
    main()
