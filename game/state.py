from collections import namedtuple
from hashlib import sha1

from .car import Car

__HEURISTIC__ = None

History = namedtuple('History', 'hist, steps, parent')

class State:
    def __init__(self, cars, history=None) -> None:
        self.cars = cars
        self.history: History = history if history is not None else History('', 0, None)

    def occupied(self, row, col) -> bool:
        for car in self.cars:
            if car.row == row and car.horz and car.col <= col < car.col + car.length:
                return car.car_id
            if car.col == col and car.vert and car.row <= row < car.row + car.length:
                return car.car_id
        return None

    def available(self, row, col) -> bool:
        if 0 <= row < 6 and 0 <= col < 6:
            return self.occupied(row, col) is None
        return False

    def span(self) -> 'State':
        for idx, car in enumerate(self.cars):
            if car.horz:
                # Left
                if self.available(car.row, car.col - 1):
                    step, new_car = car.left()
                    yield State(self.cars[:idx] + (new_car, ) + self.cars[idx + 1:], History(step, self.history.steps + 1, self.history))
                # Right
                if self.available(car.row, car.col + car.length):
                    step, new_car = car.right()
                    yield State(self.cars[:idx] + (new_car, ) + self.cars[idx + 1:], History(step, self.history.steps + 1, self.history))
            else:
                # Up
                if self.available(car.row - 1, car.col):
                    step, new_car = car.up()
                    yield State(self.cars[:idx] + (new_car, ) + self.cars[idx + 1:], History(step, self.history.steps + 1, self.history))
                # Down
                if self.available(car.row + car.length, car.col):
                    step, new_car = car.down()
                    yield State(self.cars[:idx] + (new_car, ) + self.cars[idx + 1:], History(step, self.history.steps + 1, self.history))

    @property
    def complete(self) -> bool:
        return self.cars[0].row == 2 and self.cars[0].col == 4

    @property
    def steps(self) -> int:
        return self.history.steps

    @property
    def H(self) -> int:
        global __HEURISTIC__
        h = 0
        if __HEURISTIC__ in ('2', ):
            red_car = self.cars[0]
            for car in self.cars:
                if car.car_id != 0 and car.vert and car.col >= red_car.col + red_car.length and car.row <= 2 < car.row + car.length:
                    h += 2
                    if car.length == 2:
                        if self.occupied(0, car.col) in (car.car_id, None) and self.occupied(1, car.col) in (car.car_id, None):
                            h -= 1
                        elif self.occupied(3, car.col) in (car.car_id, None) and self.occupied(4, car.col) in (car.car_id, None):
                            h -= 1
                    elif self.occupied(3, car.col) in (car.car_id, None) and self.occupied(4, car.col) in (car.car_id, None) and self.occupied(5, car.col) in (car.car_id, None):
                        h -= 1
        else:
            for col in range(self.cars[0].col + self.cars[0].length, 6):
                if self.occupied(2, col) is not None:
                    h += 1
        return h

    @property
    def hash(self) -> bytes:
        """Generate a SHA-1 hash for this state

        Directly saving a state with 8 cars requires 8*5*4*8 = 1280 bits

        Saving the state in this way only uses 160 bits

        Returns:
            bytes: the hash result
        """
        return sha1(' '.join(('%d,%d,%d,%d,%d' % (car.car_id, car.row, car.col, car.length, 1 if car.horz else 0)) for car in self.cars).encode()).digest()

    @classmethod
    def parse(cls, puzzle) -> 'State':
        return cls(tuple([Car.fromSpec(line.strip()) for line in puzzle]))
