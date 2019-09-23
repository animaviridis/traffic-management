class SuburbArea(object):
    def __init__(self, name: str, population: float):
        self._name = name
        self._population = int(population)

    def __repr__(self):
        return f"Suburb area {self._name} with population of {self.population: d}"

    @property
    def name(self):
        return self._name

    @property
    def population(self):
        return self._population


class City(object):
    def __init__(self, name=None):
        self._name = name if name is not None else ''
        self._suburbs = {}

    def __repr__(self):
        return f"City{' ' + self._name if self._name else ''} with suburb areas: {', '.join(self.suburb_names)}"

    @property
    def suburbs(self):
        return self._suburbs

    @property
    def suburb_names(self):
        return list(self._suburbs.keys())

    def add_suburb_area(self, name, *args, **kwargs):
        self._suburbs[name] = SuburbArea(name, *args, **kwargs)


if __name__ == '__main__':
    city = City("Radiator Springs")
    city.add_suburb_area('A', 30e3)
    city.add_suburb_area('B', 45e3)
    city.add_suburb_area('C', 55e3)
    city.add_suburb_area('D', 65e3)
