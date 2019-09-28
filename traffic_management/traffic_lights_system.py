from pyddl import Domain, neg
from custom_pyddl.cpyddl import Action, Problem
from custom_pyddl.cplanner import DNPlanner
from traffic_management.city import define_city

city = define_city()
city.switch_priority('', 'A')


def tnc(suburb):
    return city.suburbs[suburb].get_cars_in(20)  # TODO: time window from arg parser


def fbs(action_name, *suburbs):
    if action_name == 'switch-priority':
        time = city.tp.base_time
        suburb = suburbs[1]
        accelerating = True
    else:
        time = city.tp.ext_time
        suburb = suburbs[0]
        accelerating = False
    n = city.suburbs[suburb].get_cars_out(time, accelerating)
    # print(f"{action_name}{suburbs}: number of cars passing from {suburb}: {n}; queue: {tuple(city.queue.values())}")
    return n


a1 = Action('switch-priority',
            parameters=(('suburb', 'S1'), ('suburb', 'S2')),
            preconditions=(('prioritised', 'S1'),),  # TODO: S1 != S2 - possible?
            effects=(neg(('prioritised', 'S1')),
                     ('prioritised', 'S2'),
                     ('-=', ('total-cars', 'S2'), fbs)),
            external_actor=city
            )

a2 = Action('extend-priority',
            parameters=(('suburb', 'S'),),
            preconditions=(('prioritised', 'S'),),
            effects=(('-=', ('total-cars', 'S'), fbs),),
            external_actor=city
            )


domain = Domain((a1, a2))


problem = Problem(domain, {'suburb': tuple(city.suburb_names)},
                  init=(('prioritised', 'A'),
                        *tuple(('=', ('total-cars', s), tnc(s)) for s in city.suburb_names)),
                  goal=tuple(('<=', ('total-cars', s), 0) for s in city.suburb_names))


def plan():
    city.wait(2)

    planner = DNPlanner(problem)
    planner.solve()

    print(f"\nPriority record:")
    for s, t in city.priority_record:
        print(f"{s}: {t}")

    print(f"------------\n{dict(city.priority_summary)} "
          f"({len(city.priority_record)} changes; total time: {sum(city.priority_summary.values())})")
