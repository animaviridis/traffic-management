class SuburbArea(object):
    def __init__(self, name: str, population: float):
        self._name = name
        self._population = population

    @property
    def name(self):
        return self._name

    @property
    def population(self):
        return self._population


class City(object):
    def __init__(self):
        self._suburbs = []

    @property
    def suburbs(self):
        return self._suburbs

    def add_suburb_area(self, *args, **kwargs):
        self._suburbs.append(SuburbArea(*args, **kwargs))


if __name__ == '__main__':
    city = City()
    city.add_suburb_area('A', 30e3)
    city.add_suburb_area('B', 45e3)
    city.add_suburb_area('C', 55e3)
    city.add_suburb_area('D', 65e3)
