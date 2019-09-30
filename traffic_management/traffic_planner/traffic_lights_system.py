from argparse import ArgumentParser
from pyddl import Domain, neg

from traffic_management.custom_pyddl.action import Action
from traffic_management.custom_pyddl.problem import Problem
from traffic_management.custom_pyddl.planner import DNPlanner
from traffic_management.traffic.city import City, define_city


def define_domain(city):
    a1 = Action('switch-priority',
                parameters=(('suburb', 'S1'), ('suburb', 'S2')),
                preconditions=(('prioritised', 'S1'),),
                effects=(neg(('prioritised', 'S1')),
                         ('prioritised', 'S2'),
                         ('-=', ('total-cars', 'S2'), city.get_cars_out_from_action)),
                external_actor=city,
                unique=True
                )

    a2 = Action('extend-priority',
                parameters=(('suburb', 'S'),),
                preconditions=(('prioritised', 'S'),),
                effects=(('-=', ('total-cars', 'S'), city.get_cars_out_from_action),),
                external_actor=city
                )

    return Domain((a1, a2))


def define_problem(city, time_window=20):
    def tot_cars(suburb):
        return city.suburbs[suburb].get_cars_in(time_window)

    domain = define_domain(city)
    problem = Problem(domain, {'suburb': tuple(city.suburb_names)},
                      init=(('prioritised', city.prioritised),
                            *tuple(('=', ('total-cars', s), tot_cars(s)) for s in city.suburb_names)),
                      goal=tuple(('<=', ('total-cars', s), 0) for s in city.suburb_names))

    return problem


def make_plan(city, problem):
    planner = DNPlanner(problem)
    plan = planner.solve()

    print(f"\nPriority record:")
    for s, t in city.priority_record:
        print(f"{s}: {t}")

    print(f"------------\n{dict(city.priority_summary)} "
          f"({len(city.priority_record)} changes; total time: {sum(city.priority_summary.values())})")

    return plan


def parse_args():
    parser = ArgumentParser(description="Traffic problem solver argument parser", parents=[City.define_parser()])
    parser.add_argument('--time-window', default=5, type=float, help="Analysis time window")
    parser.add_argument('--initial-priority', default='A',
                        help="Area to which th priority should be switched before start of the analysis")
    parser.add_argument('--init-wait', type=float, default=3,
                        help="Waiting time [min] to be applied to all suburb areas before the analysis "
                             "(to accumulate some cars in front of the junction)")
    return parser.parse_args()


def main():
    parsed_args = parse_args()

    city = define_city(parsed_args=parsed_args)
    city.wait(parsed_args.init_wait)
    city.switch_priority('', parsed_args.initial_priority)

    problem = define_problem(city, time_window=parsed_args.time_window)
    make_plan(city, problem)


if __name__ == '__main__':
    main()
