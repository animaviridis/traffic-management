from collections import defaultdict
from argparse import ArgumentParser

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
        self.evaluate_action = {f: self.evaluate_priority_decision for f in ('switch-priority', 'extend-priority')}

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
        self._suburbs[name] = SuburbArea(name, *args, traffic_properties=self.tp, **kwargs)

    def wait(self, time=1):
        for suburb in self.suburbs.values():
            if not suburb.prioritised:
                suburb.wait(time)

    def switch_priority(self, s1, s2, time=None):
        time = time or self.tp.base_time

        if s1:
            if not self.suburbs[s1].prioritised:
                raise ValueError(f"{s1} is not currently prioritised")
            self.suburbs[s1].unprioritise()

        self.suburbs[s2].prioritise()
        self.prioritised = s2
        self.priority_record.append((s2, time))
        self._apply_priority(time)
        print(f"Switched to {s2}; queue: {tuple(self.queue.values())}")

    def extend_priority(self, s, time=None):
        time = time or self.tp.ext_time
        if not self.suburbs[s].prioritised:
            raise ValueError(f"{s} is not currently prioritised")

        self.priority_record[-1] = (s, self.priority_record[-1][1] + time)
        self._apply_priority(time)
        print(f"Extended {s}; queue: {tuple(self.queue.values())}")

    def _apply_priority(self, time):
        s = self.prioritised
        self.suburbs[s].go(time)
        self.wait(time)
        self.priority_summary[s] += time

    def evaluate_priority_decision(self, *suburbs, time=None):
        s = suburbs[-1]
        time = time or (self.tp.base_time if len(suburbs) > 1 else self.tp.ext_time)
        return (self.get_cars_out(s, time) - self.tp.wait_factor * self.get_acc_waiting_time(s, time)) / time

    def get_acc_waiting_time(self, s_prioritised, time):
        acc_waiting_time = 0
        for suburb in self.suburbs.values():
            if suburb.name != s_prioritised:
                acc_waiting_time += suburb.accumulated_waiting_time(time)
        return acc_waiting_time

    def get_cars_out(self, s_prioritised, time=None):
        return self.suburbs[s_prioritised].get_cars_out(time)

    def get_cars_out_from_action(self, *args):
        return self.get_cars_out(args[-1])

    @property
    def queue(self):
        return {s.name: s.queue for s in self.suburbs.values()}

    @property
    def population(self):
        return sum(s.population for s in self.suburbs.values())

    @staticmethod
    def define_parser():
        parser = ArgumentParser(description="City class argument parser", parents=[TrafficProperties.define_parser()],
                                add_help=False)
        parser.add_argument('--name', type=str, default="Radiator Springs", help="City name")

    @staticmethod
    def from_parser(parsed_args=None):
        tp = TrafficProperties.from_parser(parsed_args) if parsed_args else None
        return City(parsed_args.name if parsed_args else "Radiator Springs", traffic_properties=tp)


def define_city(parsed_args=None):
    city = City.from_parser(parsed_args)
    city.add_suburb_area('A', 30e3)
    city.add_suburb_area('B', 45e3)
    city.add_suburb_area('C', 55e3)
    city.add_suburb_area('D', 65e3)
    return city


if __name__ == '__main__':
    define_city()
