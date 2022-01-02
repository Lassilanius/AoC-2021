from pathlib import Path
import time

paths = [Path(__file__).with_name('sample.txt'), Path(__file__).with_name('input.txt')]

class Amphipods:

    costOfMove            = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    occupiableHallIndices = (0, 1, 3, 5, 7, 9, 10)
    nrOfRooms             = 4
    letters               = "ABCD"

    def __init__(self, rooms, hall, nrOfLetters, energy = 0):
        self.rooms       = rooms
        self.hall        = hall
        self.energy      = energy
        self.nrOfLetters = nrOfLetters

    def __str__(self):
        a = '#############\n'
        b = '#' + ''.join(self.hall) + "#\n"
        c = '###' + '#'.join(x[-1] if self.nrOfLetters == len(x) else '.' for x in self.rooms) + '###\n'
        s = a + b + c
        for i in range(self.nrOfLetters - 2, -1, -1):
            s += '  #' + '#'.join(x[i] if i < len(x) else '.' for x in self.rooms) + '#\n'
        s += '  #########\n'
        return s

    def stepsRoomToHall(self, roomIdx, hallIdx):
        room   = self.rooms[roomIdx]
        hall   = self.hall
        steps  = self.nrOfLetters - len(room) + 1
        i = roomIdx * 2 + 2
        xs = range(i + 1, hallIdx + 1) if i < hallIdx else range(hallIdx, i)
        for x in xs:
            if hall[x] != '.': # Path is blocked
                return None
            steps += 1
        return steps

    def stepsHallToRoom(self, hallIdx, roomIdx):
        i     = roomIdx * 2 + 2
        hall  = self.hall
        steps = 0
        xs = range(i, hallIdx) if i < hallIdx else range(hallIdx + 1, i + 1)
        for x in xs:
            if hall[x] != '.': # Path is blocked
                return None
            steps += 1
        return steps + self.nrOfLetters - len(self.rooms[roomIdx])
    
    def stepsRoomToRoom(self, r1, r2):
        a = self.stepsRoomToHall(r1, r1 * 2 + 2)
        if a:
            b = self.stepsHallToRoom(r1 * 2 + 2, r2)
            if b:
                return a + b

    def isOrganized(self):
        return all(len(x) == self.nrOfLetters for x in self.rooms) and \
               all(all(x == y for x in room) for room, y in zip(self.rooms, Amphipods.letters))

    def organize(self):

        if self.isOrganized():
            return self.energy

        # Try moving a letter from the hall to its corresponding room
        for hallIdx, x in enumerate(self.hall):
            if x in Amphipods.letters:
                roomIdx = Amphipods.letters.index(x)
                if not self.rooms[roomIdx] or all(y == x for y in self.rooms[roomIdx]):
                    steps = self.stepsHallToRoom(hallIdx, roomIdx)
                    if steps:
                        self.hall[hallIdx] = '.'
                        self.rooms[roomIdx].append(x)
                        return Amphipods(self.rooms,
                                        self.hall,
                                        self.nrOfLetters,
                                        self.energy + steps * Amphipods.costOfMove[x]).organize()

        # Try moving a letter from a wrong room to its correct room
        for roomIdx in range(Amphipods.nrOfRooms):
            if not self.rooms[roomIdx]:
                continue
            x = self.rooms[roomIdx][-1]
            if x != Amphipods.letters[roomIdx]:
                i = Amphipods.letters.index(x)
                if not self.rooms[i] or all(y == x for y in self.rooms[i]):
                    steps = self.stepsRoomToRoom(roomIdx, i)
                    if steps:
                        self.rooms[roomIdx].pop()
                        self.rooms[i].append(x)
                        return Amphipods(self.rooms,
                                        self.hall,
                                        self.nrOfLetters,
                                        self.energy + steps * Amphipods.costOfMove[x]).organize()

        # Try moving letters from wrong rooms to the hall
        minEnergy = float('inf')
        for roomIdx in range(Amphipods.nrOfRooms):
            if not self.rooms[roomIdx]:
                continue
            x = self.rooms[roomIdx][-1]
            if x != Amphipods.letters[roomIdx] or \
               x == Amphipods.letters[roomIdx] and any(y != x for y in self.rooms[roomIdx]):
                for j in Amphipods.occupiableHallIndices:
                    if self.hall[j] == '.':
                        steps = self.stepsRoomToHall(roomIdx, j)
                        if steps:
                            roomsCopy = [x[:] for x in self.rooms]
                            hallCopy  = self.hall[:]
                            self.rooms[roomIdx].pop()
                            self.hall[j] = x
                            energy = Amphipods(self.rooms,
                                               self.hall,
                                               self.nrOfLetters,
                                               self.energy + steps * Amphipods.costOfMove[x]).organize()
                            self.rooms = roomsCopy
                            self.hall  = hallCopy
                            minEnergy  = min(energy, minEnergy)

        return minEnergy

def main():
    for p in paths:
        with p.open('r') as f:
            t0    = time.time()
            inp   = f.read().split('\n')
            rooms = [[*[*zip(*inp)][i][3:1:-1]] for i in range(3, 10, 2)]
            hall  = ['.'] * 11
            amphi = Amphipods(rooms, hall, 2)

            print(amphi.organize())
            print(f'Run time for part 1 in seconds: {time.time() - t0}')

            t0    = time.time()
            inp   = inp[:3] + ['  #D#C#B#A#', '  #D#B#A#C#'] + inp[3:]
            rooms = [[*[*zip(*inp)][i][5:1:-1]] for i in range(3, 10, 2)]
            hall  = ['.'] * 11
            amphi = Amphipods(rooms, hall, 4)

            print(amphi.organize())
            print(f'Run time for part 2 in seconds: {time.time() - t0}')

if __name__ == '__main__':
    main()
