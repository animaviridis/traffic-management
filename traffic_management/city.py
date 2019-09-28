from collections import defaultdict
from traffic_management.traffic import TrafficProperties
from traffic_management.suburb_area import SuburbArea
        

class City(object):
    def __init__(self, name: str = None, traffic_properties=None):
        self._name = name if name is not None else ''
        self.tp = traffic_properties or TrafficProperties()

        self._suburbs = {}
        self.prioritised = ''

        self.apply_action = {'switch-priority': self.switch_priority,
                             'extend-priority': self.extend_priority}
        self.evaluate_action = {'switch-priority': self.evaluate_switch_priority,
                                'extend-priority': self.evaluate_extend_priority}

        self.priority_record = []
        self.priority_summary = defaultdict(lambda: 0)

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
        print(f"Switching to {s2}; queue: {tuple(self.queue.values())}")
        if s1:
            if not self.suburbs[s1].prioritised:
                raise ValueError(f"{s1} is not currently prioritised")
            self.suburbs[s1].unprioritise()

        self.suburbs[s2].prioritise()
        self.prioritised = s2
        self.suburbs[s2].go(self.tp.base_time, accelerating=True)

        self.wait(self.tp.base_time)
        self.priority_record.append((s2, self.tp.base_time))
        self.priority_summary[s2] += self.tp.base_time

    def extend_priority(self, s):
        print(f"Extending {s}; queue: {tuple(self.queue.values())}")

        if not self.suburbs[s].prioritised:
            raise ValueError(f"{s} is not currently prioritised")

        self.wait(self.tp.ext_time)
        self.suburbs[self.prioritised].go(self.tp.ext_time, accelerating=False)

        self.priority_record[-1] = (s, self.priority_record[-1][1] + self.tp.ext_time)
        self.priority_summary[s] += self.tp.ext_time

    def evaluate_switch_priority(self, s1, s2):
        return self._get_total_acc_waiting_time(s2, self.tp.base_time)

    def evaluate_extend_priority(self, s):
        return self._get_total_acc_waiting_time(s, self.tp.ext_time)

    def _get_total_acc_waiting_time(self, s_prioritised, time):
        acc_waiting_time = 0
        for suburb in self.suburbs.values():
            if suburb.name != s_prioritised:
                acc_waiting_time += suburb.accumulated_waiting_time(time)

        return (self._get_cars_out(s_prioritised) - self.tp.wait_factor * acc_waiting_time) / time

    def _get_cars_out(self, s_prioritised):
        change = s_prioritised != self.prioritised
        time = self.tp.ext_time if change else self.tp.base_time
        return self.suburbs[s_prioritised].get_cars_out(time, change)

    @property
    def queue(self):
        return {s.name: s.queue for s in self.suburbs.values()}

    @property
    def population(self):
        return sum(s.population for s in self.suburbs.values())


def define_city():
    city = City("Radiator Springs")
    city.add_suburb_area('A', 30e3)
    city.add_suburb_area('B', 45e3)
    city.add_suburb_area('C', 55e3)
    city.add_suburb_area('D', 65e3)
    return city


if __name__ == '__main__':
    define_city()
