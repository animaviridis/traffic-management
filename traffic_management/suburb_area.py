from traffic_management.traffic import TrafficProperties


class SuburbArea(object):
    def __init__(self, name: str, population: float, traffic_properties=None):
        self._name = name
        self._population = int(population)

        self.tp = traffic_properties or TrafficProperties()
        self.flow = self.tp.FLOW_FACTOR * self.population
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
        if self.prioritised:
            raise RuntimeError(f"Suburb {self.name} is currently prioritised - 'wait' not applicable")

        self.queue += self.get_cars_in(time)
        self.waiting_time += time

    def go(self, time, accelerating=False):
        if not self.prioritised:
            raise RuntimeError(f"Suburb {self.name} is not currently prioritised - 'go' not applicable")

        n_cars_passing = self.get_cars_out(time, accelerating)
        self.queue -= (n_cars_passing - self.get_cars_in(time))  # TODO: verify

    def prioritise(self):
        self.prioritised = True
        self.waiting_time = 0

    def unprioritise(self):
        self.prioritised = False

    def accumulated_waiting_time(self, add_time):
        return 0.5 * self.flow * (self.waiting_time + add_time) ** 2  # [cars * minutes]

    def get_cars_in(self, time):
        return int(self.flow * time)

    def get_cars_out(self, time, accelerating=False):
        """Number of cars which can pass through the junction in given time.

        The number of cars is the minimum of two following quantities:
            - all cars currently in the queue plus inflow in the given time (full queue unloading case)
            - number of cars which can pass through the junction in the given time, given max junction flow
                (partial queue unloading case); this also takes into account initial acceleration, whose time is
                assumed to be always smaller than the pass time."""

        n_full_unloading = self.queue + self.get_cars_in(time)
        n_partial_unloading = self.tp.junction_flow * (time - accelerating * 0.5 * self.tp.acc_time)

        return int(min(n_full_unloading, n_partial_unloading))  # round down to nearest integer
