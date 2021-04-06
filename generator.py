import random
import queue
from game.state import State


def occupied(cars, r, c):
    if r < 0 or r >= 5 or c < 0 or c >= 5:
        return True
    if r == 2 and c >= cars[0][2]:
        return True
    for row, col, length, orient in cars:
        if row == r and orient == 1 and col <= c < col + length:
            return True
        if col == c and orient == 2 and row <= r < row + length:
            return True
    return False


def gen():
    n = random.randint(5, 11)
    cars = [(2, random.randint(0, 2), 2, 1)]

    blockers = random.randint(3 if n > 7 else 2, 4 if n > 9 else (3 if n > 7 else 2))
    if blockers == 2:
        length = random.randint(2, 3)
        if length == 3:
            cars.append((3, 4, 3, 2))
        else:
            cars.append(
                (random.randint(3, 4) if random.randint(0, 2) else 0, 4, 2, 2))
        length = random.randint(2, 3)
        if length == 3:
            cars.append((3, 5, 3, 2))
        else:
            cars.append(
                (random.randint(3, 4) if random.randint(0, 2) else 0, 5, 2, 2))
    else:
        col = random.randint(4, 5)
        cars.append((0, col, 2, 2))
        cars.append((3, col, 3, 2))
        length = random.randint(2, 3)
        if length == 3:
            cars.append((3, 4 if col == 5 else 5, 3, 2))
        else:
            cars.append(
                (random.randint(3, 4) if random.randint(0, 2) else 0, 4 if col == 5 else 5, 2, 2))
        if blockers == 4:
            cars.append(
                (random.randint(3, 4) if random.randint(0, 2) else 0, 3, 2, 2))
    n -= blockers

    fail = 0
    while n > 0 and fail < 50:
        orient = 1 if random.randint(0, 2) else 2
        length = 2 if random.randint(0, 2) else 3
        r = random.randint(0, 6 - length if orient == 2 else 5)
        c = random.randint(0, 6 - length if orient == 1 else 2)
        ok = True
        for i in range(length):
            if occupied(cars, r if orient == 1 else r + i, c if orient == 2 else c + i):
                ok = False
                break
        if ok:
            cars.append((r, c, length, orient))
            fail = 0
        else:
            fail += 1

    puzzle = ['%d %d %d %d %d' % (idx, *car) for idx, car in enumerate(cars)]
    init_state = State.parse(puzzle)
    node_exp = 0
    presense = set()
    frontier = queue.Queue()
    presense.add(init_state.hash)
    frontier.put(init_state)
    front = None
    while node_exp < 20000:
        if frontier.empty():
            break
        front = frontier.get()
        if front.complete:
            continue
        for span in front.span():
            if span.hash not in presense:
                presense.add(span.hash)
                frontier.put(span)
                node_exp += 1
    puzzle = '\n'.join(['%d %d %d %d %d' % (car._car_id, car._row, car._col, car._length, car._orient) for car in front.cars])
    return puzzle


if __name__ == '__main__':
    print(gen())
