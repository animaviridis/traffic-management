from traffic_management.traffic.traffic_properties import TrafficProperties


class SuburbArea(object):
    """Model of a suburb area - component of the city."""

    def __init__(self, name: str, population: float, traffic_properties=None):
        self._name = name
        self._population = int(population)

        self.tp = traffic_properties or TrafficProperties()
        self.queue = 0  # number of cars waiting in front of the junction
        self.last_passed = 0  # number of cars that have passed in the last (current) priority setting
        self.waiting_time = 0
        self.prioritised = False

    def __repr__(self):
        return f"Suburb area {self._name} with population of {self.population: d}"

    @property
    def flow(self):
        return self.tp.flow_factor * self.population

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

    def go(self, time):
        if not self.prioritised:
            raise RuntimeError(f"Suburb {self.name} is not currently prioritised - 'go' not applicable")

        n_cars_passing = self.get_cars_out(time)
        self.queue -= (n_cars_passing - self.get_cars_in(time))  # TODO: verify
        self.last_passed += n_cars_passing

    def prioritise(self):
        self.prioritised = True
        self.waiting_time = 0

    def unprioritise(self):
        self.prioritised = False
        self.last_passed = 0

    def accumulated_waiting_time(self, add_time):
        return 0.5 * self.flow * (self.waiting_time + add_time) ** 2  # [cars * minutes]

    def get_cars_in(self, time):
        return int(self.flow * time)

    def get_cars_out(self, time=None):
        """Number of cars which can pass through the junction in given time.

        The number of cars is the minimum of two following quantities:
            - all cars currently in the queue plus inflow in the given time (full queue unloading case)
            - number of cars which can pass through the junction in the given time, given max junction flow
                (partial queue unloading case).

        If the was not currently prioritised, the latter takes into account initial acceleration.
        """

        if self.last_passed:
            delay = 0
            time = time or self.tp.ext_time
        else:
            delay = 0.5 * self.tp.acc_time
            time = time or self.tp.base_time

        if delay > time:
            raise ValueError(f"Initial priority time: {time} min too short (must be at least {delay} min)")

        n_partial_unloading = self.tp.junction_flow * (time - delay)

        n_full_unloading = self.queue + self.get_cars_in(time)

        return int(min(n_full_unloading, n_partial_unloading))  # round down to nearest integer
