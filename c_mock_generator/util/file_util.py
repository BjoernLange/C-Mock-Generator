from typing import List


def read_lines(filename: str) -> List[str]:
    with open(filename) as file:
        return [line.rstrip() for line in file.readlines()]
