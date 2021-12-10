from pathlib import Path

paths = [Path(__file__).with_name('sample_input.txt'), Path(__file__).with_name('input.txt')]

def countUniqueLenDigits(data):
    return sum(1 for _, x in data for y in x if len(y) in (2, 3, 4, 7))

def encode(patterns):
    patterns = [*map(set, sorted(patterns, key = len))]
    digits   = [''] * 10
    digits[1], digits[7], digits[4] = patterns[:3]
    digits[8] = patterns[-1]
    fiveLetterDigits, sixLetterDigits = patterns[3: 6], patterns[6: 9]
    digits[2] = next(x for x in fiveLetterDigits if len(x.intersection(digits[4])) == 2)
    digits[3] = next(x for x in fiveLetterDigits if not digits[1].difference(x))
    digits[5] = next(x for x in fiveLetterDigits if x != digits[2] and x != digits[3])
    digits[6] = next(x for x in sixLetterDigits if len(x.intersection(digits[1])) == 1)
    digits[9] = next(x for x in sixLetterDigits if not digits[4].difference(x))
    digits[0] = next(x for x in sixLetterDigits if x != digits[6] and x != digits[9])
    return {''.join(digits[i]): str(i) for i in range(10)}

def sumOutputValues(data):
    res = 0
    for patterns, output in data:
        table = encode(patterns)
        res += int(''.join(next(table[k] for k in table if set(k) == set(x)) for x in output))
    return res

def main():
    for p in paths:
        with p.open('r') as f:
            data = [tuple(map(str.split, line.split('|'))) for line in f.readlines()]
            print(countUniqueLenDigits(data))
            print(sumOutputValues(data))

if __name__ == '__main__':
    main()
