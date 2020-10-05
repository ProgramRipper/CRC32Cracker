POLY = 0xEDB88320


class crc32Cracker:
    def __init__(self):
        self.table = self.table()

    def crc32(self, string: str) -> (int, int):
        INIT = 0xFFFFFFFF
        index = None
        for i in string:
            index = (INIT ^ ord(i)) & 0xFF
            INIT = INIT >> 8 ^ self.table[index]
        return INIT, index

    def lastIndex(self, crc: int) -> int:
        for i in range(256):
            if crc == self.table[i] >> 24:
                return i

    def check(self, high: int, indexes: list) -> (bool, str):
        crc, index = self.crc32(str(high))
        if index != indexes[3]:
            return False
        low = ''
        for i in range(2, -1, -1):
            num = crc & 0xFF ^ indexes[i]
            if num not in range(48, 58):
                return False
            low += str(num - 48)
            crc = self.table[indexes[i]] ^ crc >> 8
        return low

    @staticmethod
    def table():
        table = []
        for i in range(256):
            value = i
            for _ in range(8):
                if value & 1:
                    value = value >> 1 ^ POLY
                else:
                    value >>= 1
            table.append(value)
        return table

    def main(self, crc):
        indexes = [0 for _ in range(4)]
        crc = int(crc, 16) ^ 0xFFFFFFFF
        for i in range(1, 1000):
            if crc == self.crc32(str(i))[0]:
                return i
        for i in range(3, -1, -1):
            index = indexes[3 - i] = self.lastIndex(crc >> (i << 3))
            value = self.table[index]
            crc ^= value >> ((3 - i) << 3)
        i = 0
        while True:
            i += 1
            low = self.check(i, indexes)
            if low:
                return int(str(i) + low)

    def __call__(self, crc):
        return self.main(crc)


if __name__ == '__main__':
    from time import time
    from sys import argv

    cracker = crc32Cracker()
    t = time()
    print(cracker(argv[1]), time() - t)
