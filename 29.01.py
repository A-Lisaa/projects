from typing import Any


def count_(lis: list[Any], item: Any) -> int:
    amount = 0
    for elem in lis:
        if elem == item:
            amount += 1
    return amount

def index_(lis: list[Any], item: Any) -> int:
    for i, elem in enumerate(lis):
        if elem == item:
            return i
    return -1

def insert_(lis: list[Any], index: int, item: Any) -> list[Any]:
    lis.append(0)
    if index < 0:
        index = len(lis) + index - 1
    for i in range(len(lis)-2, index-1, -1):
        lis[i+1] = lis[i]
    lis[index] = item
    return lis


if __name__ == "__main__":
    mas = [1, 8, 684, 13, 86, 1, 431, 1, 465, 15]

    print("Начальный список: ", mas)

    print("count_(mas, 1): ", count_(mas, 1))

    print("index_(mas, 684):", index_(mas, 684))

    print("insert_(mas, -2, 1488): ", insert_(mas, -2, 1488))
