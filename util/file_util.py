from typing import List


def read_lines(filename: str) -> List[str]:
    with open(filename) as file:
        return [l.rstrip() for l in file.readlines()]
