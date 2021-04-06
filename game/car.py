class Car:
    cars = {}

    def __init__(self, car_id, row, col, length, orient):
        self._car_id = int(car_id)
        self._row = int(row)
        self._col = int(col)
        self._length = int(length)
        self._orient = int(orient)
    
    def up(self):
        return ('%d %d %d' % (self._car_id, self._row - 1, self._col)), self.get(self._row - 1, self._col)
    
    def down(self):
        return ('%d %d %d' % (self._car_id, self._row + 1, self._col)), self.get(self._row + 1, self._col)
    
    def left(self):
        return ('%d %d %d' % (self._car_id, self._row, self._col - 1)), self.get(self._row, self._col - 1)
    
    def right(self):
        return ('%d %d %d' % (self._car_id, self._row, self._col + 1)), self.get(self._row, self._col + 1)

    def get(self, row, col):
        old = Car.cars.get((self._car_id, row, col), None)
        if old is not None:
            return old
        new = Car(self._car_id, row, col, self._length, self._orient)
        Car.cars[(self._car_id, row, col)] = new
        return new
    
    @classmethod
    def fromSpec(cls, spec):
        car_id, row, col, length, orient = spec.split()
        return cls(car_id, row, col, length, orient)

    @property
    def car_id(self):
        return self._car_id

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def length(self):
        return self._length

    @property
    def horz(self):
        return self._orient == 1

    @property
    def vert(self):
        return not self.horz
