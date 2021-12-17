from pathlib import Path
from operator import add, mul, gt, lt, eq
from functools import reduce

path = Path(__file__).with_name('input.txt')

class PacketDecoder:

    typeIdToOperator = {0: add, 1: mul, 2: min, 3: max, 5: gt, 6: lt, 7: eq}

    def __init__(self, hexString):
        self.hexString   = hexString
        self.bits        = PacketDecoder.hexToBin(hexString)
        self.versionNums = []
        self.ptr         = 0

    @staticmethod
    def hexToBin(hexString):
        return ''.join(bin(int(x, 16))[2:].rjust(4, '0') for x in hexString)

    def interpret(self):
        bits, ptr = self.bits, self.ptr
        self.versionNums.append(int(bits[ptr: ptr + 3], 2))
        typeId = int(bits[ptr + 3: ptr + 6], 2)
        ptr += 6

        if typeId == 4:
            val = ''
            while bits[ptr] == '1':
                val += bits[ptr + 1: ptr + 5]
                ptr += 5
            val += bits[ptr + 1: ptr + 5]
            self.ptr = ptr + 5
            return int(val, 2)

        subPacks = []
        if bits[ptr] == '0':
            numBits = int(bits[ptr + 1: ptr + 16], 2)
            ptr += 16
            self.ptr = ptr
            while numBits > 0:
                subPacks.append(self.interpret())
                numBits += ptr - self.ptr
                ptr     += self.ptr - ptr
                self.ptr = ptr
        else:
            numSubPacks = int(bits[ptr + 1: ptr + 12], 2)
            self.ptr = ptr + 12
            for _ in range(numSubPacks):
                subPacks.append(self.interpret())

        return int(reduce(PacketDecoder.typeIdToOperator[typeId], subPacks))


def main():
    with path.open('r') as f:
        data = f.read()
        sampleData = [("C200B40A82", 3),
                      ("04005AC33890", 54),
                      ("880086C3E88112", 7),
                      ("CE00C43D881120", 9),
                      ("D8005AC2A8F0", 1),
                      ("F600BC2D8F", 0),
                      ("9C005AC2F8F0", 0),
                      ("9C0141080250320F1802104A08", 1)]
        for packet, expectedVal in sampleData:
            decoder = PacketDecoder(packet)
            actualVal = decoder.interpret()
            try:
                assert actualVal == expectedVal
            except AssertionError:
                print(f'Decoding of packet {packet} failed: {actualVal} should equal {expectedVal}')

        decoder = PacketDecoder(data)
        val = decoder.interpret()
        print(sum(decoder.versionNums))
        print(val)

if __name__ == '__main__':
    main()
