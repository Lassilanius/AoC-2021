from pathlib import Path
from itertools import islice
from functools import reduce
from operator import add
from math import floor, ceil

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

class TreeList:

    maxDepth = 4
    maxValue = 9

    def __init__(self, left = None, right = None, parent = None, value = 0):
        self.left   = left
        self.right  = right
        self.parent = parent
        self.value  = value

    @classmethod
    def fromList(cls, l):
        if isinstance(l, list):
            left  = cls.fromList(l[0])
            right = cls.fromList(l[1])
            node  = TreeList(left, right)
            left.setParent(node)
            right.setParent(node)
            return node
        return TreeList(value = l)

    def __str__(self):
        if self.left and self.right:
            return ''.join(f'[{str(self.left)}, {str(self.right)}]')
        return str(self.value)

    def __add__(self, other):
        root = TreeList(self, other)
        self.parent  = root
        other.parent = root
        while root.explodes() or root.splits():
            pass
        return root

    def setParent(self, parent):
        self.parent = parent

    def clear(self):
        self.left  = None
        self.right = None
        self.value = 0

    def getAdjacentLeafs(self):
        ''' Return the left and right adjacent leafs as a tuple (left, right). '''
        adjLeafs = [None, None]
        for side, otherSide in ('left', 'right'), ('right', 'left'):
            node = self
            while node.parent and getattr(node.parent, side) == node:
                node = node.parent
            if node.parent is None:
                continue
            node = getattr(node.parent, side)
            while getattr(node, otherSide):
                node = getattr(node, otherSide)
            adjLeafs[side == 'right'] = node
        return tuple(adjLeafs)

    def explodes(self, lvl = 0):
        if self.left and self.left.explodes(lvl + 1):
            return True
        if self.right and self.right.explodes(lvl + 1):
            return True
        if lvl > TreeList.maxDepth:
            node = self.parent
            lval = node.left.value
            rval = node.right.value
            node.clear()
            leftAdjLeaf, rightAdjLeaf = node.getAdjacentLeafs()
            if leftAdjLeaf:  leftAdjLeaf.value  += lval
            if rightAdjLeaf: rightAdjLeaf.value += rval
            return True
        return False

    def splits(self):
        if self.left and self.left.splits():
            return True
        if self.right and self.right.splits():
            return True
        if self.value > TreeList.maxValue:
            self.left  = TreeList(parent = self, value = floor(self.value / 2))
            self.right = TreeList(parent = self, value = ceil(self.value / 2))
            self.value = 0
            return True
        return False

    def magnitude(self):
        if self.left and self.right:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        return self.value

def solveA(data):
    return reduce(add, map(TreeList.fromList, data)).magnitude()

def solveB(data):
    maxMag = 0
    for i, x in enumerate(data):
        for y in islice(data, i, None):
            magA = (TreeList.fromList(x) + TreeList.fromList(y)).magnitude()
            magB = (TreeList.fromList(y) + TreeList.fromList(x)).magnitude()
            maxMag = max(maxMag, magA, magB)
    return maxMag

def main():
    for p in paths:
        with p.open('r') as f:
            data = [*map(eval, f.read().split('\n'))]
            print(solveA(data))
            print(solveB(data))

if __name__ == '__main__':
    main()
