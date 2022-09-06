from itertools import count
from typing import Literal

POLY: Literal[0xEDB88320] = 0xEDB88320

table: list[int] = []

for i in range(256):
    value = i
    for _ in range(8):
        if value & 1:
            value = value >> 1 ^ POLY
        else:
            value >>= 1
    table.append(value)


def crc32(string: str) -> tuple[int, int]:
    crc: int = 0xFFFFFFFF
    index: int = 0xFF
    for i in string:
        index = (crc ^ ord(i)) & 0xFF
        crc = crc >> 8 ^ table[index]
    return crc, index


def last_index(crc: int) -> int:  # type: ignore
    for index, value in enumerate(table):
        if crc == value >> 24:
            return index


def check(high: int, indexes: list) -> int | None:
    crc, index = crc32(str(high))
    if index != indexes[3]:
        return
    high *= 1000
    for i in range(2, -1, -1):
        num = (crc & 0xFF ^ indexes[i]) - 48
        if not 0 <= num < 10:
            return
        high += num * 10 ** i
        crc = table[indexes[i]] ^ crc >> 8
    return high


def main(crc: str | int) -> int:  # type: ignore
    indexes = [0] * 4
    crc = (crc if isinstance(crc, int) else int(crc, 16)) ^ 0xFFFFFFFF
    for i in range(1, 1000):
        if crc == crc32(str(i))[0]:
            return i
    for i in range(3, -1, -1):
        index = indexes[3 - i] = last_index(crc >> (i << 3))
        crc ^= table[index] >> ((3 - i) << 3)
    for i in count(1):
        if result := check(i, indexes):
            return result


if __name__ == "__main__":
    from sys import argv

    print(main(argv[1]))
