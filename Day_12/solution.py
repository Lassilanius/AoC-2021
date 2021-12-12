from pathlib import Path
from collections import defaultdict

paths = [Path(__file__).with_name('sample_input.txt'),
         Path(__file__).with_name('sample_input2.txt'),
         Path(__file__).with_name('input.txt')]

def countPaths(graph, useSmallTwice = False):

    def genPaths(path = ['start'], usedSmallTwice = False):
        if path[-1] == 'end':
            yield path[:]
            return
        for x in graph[path[-1]]:
            if x.isupper() or x not in path:
                path.append(x)
                yield from genPaths(path, usedSmallTwice)
                path.pop()
            elif not usedSmallTwice:
                path.append(x)
                yield from genPaths(path, True)
                path.pop()

    return sum(1 for _ in genPaths(usedSmallTwice = not useSmallTwice))

def main():
    for p in paths:
        with p.open('r') as f:
            connections = [tuple(x.split('-')) for x in f.read().split('\n')]
            graph       = defaultdict(list)
            for a, b in connections:
                if b != 'start': graph[a].append(b)
                if a != 'start': graph[b].append(a)
            print(countPaths(graph))
            print(countPaths(graph, useSmallTwice = True))

if __name__ == '__main__':
    main()
