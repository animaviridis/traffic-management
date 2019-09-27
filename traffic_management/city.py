from traffic_management.traffic import TrafficProperties


class SuburbArea(object):
    def __init__(self, name: str, population: float):
        self._name = name
        self._population = int(population)
        self.flow = TrafficProperties.FLOW_FACTOR * self.population
        self.queue = 0
        self.waiting_time = 0
        self.prioritised = False

    def __repr__(self):
        return f"Suburb area {self._name} with population of {self.population: d}"

    @property
    def name(self):
        return self._name

    @property
    def population(self):
        return self._population

    def wait(self, time=1):
        self.queue += self.get_inflow(time)
        self.waiting_time += time

    def prioritise(self):
        self.prioritised = True
        self.queue = 0  # assume that the junction flow is big enough for all cars to pass  # TODO
        self.waiting_time = 0

    def unprioritise(self):
        self.prioritised = False

    @property
    def accumulated_waiting_time(self):
        return 0.5 * self.flow * self.waiting_time**2  # [cars * minutes]

    def get_inflow(self, time):
        return self.flow * time


class City(object):
    def __init__(self, name: str = None):
        self._name = name if name is not None else ''
        self._suburbs = {}
        self.prioritised = ''

    def __repr__(self):
        return f"City{' ' + self._name if self._name else ''} with suburb areas: {', '.join(self.suburb_names)}"

    @property
    def name(self):
        return self._name

    @property
    def suburbs(self):
        return self._suburbs

    @property
    def suburb_names(self):
        return list(self._suburbs.keys())

    def add_suburb_area(self, name, *args, **kwargs):
        self._suburbs[name] = SuburbArea(name, *args, **kwargs)

    def wait(self, time=1):
        for suburb in self.suburbs.values():
            if not suburb.prioritised:
                suburb.wait(time)

    def switch_priority(self, s1, s2):
        if s1:
            if not self.suburbs[s1].prioritised:
                raise ValueError(f"{s1} is not currently prioritised")
            self.suburbs[s1].unprioritise()
        self.suburbs[s2].prioritise()
        self.prioritised = s2

        self.wait(TrafficProperties.PRIORITY_MIN_DURATION)

    def extend_priority(self, s):
        if not self.suburbs[s].prioritised:
            raise ValueError(f"{s} is not currently prioritised")

        self.wait(TrafficProperties.PRIORITY_EXT_DURATION)


if __name__ == '__main__':
    city = City("Radiator Springs")
    city.add_suburb_area('A', 30e3)
    city.add_suburb_area('B', 45e3)
    city.add_suburb_area('C', 55e3)
    city.add_suburb_area('D', 65e3)
