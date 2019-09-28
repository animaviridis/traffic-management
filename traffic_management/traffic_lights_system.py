from pyddl import Domain, neg
from custom_pyddl.action import Action
from custom_pyddl.problem import Problem
from custom_pyddl.planner import DNPlanner
from traffic_management.city import define_city

city = define_city()
city.switch_priority('', 'A')

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


domain = Domain((a1, a2))


problem = Problem(domain, {'suburb': tuple(city.suburb_names)},
                  init=(('prioritised', 'A'),
                        *tuple(('=', ('total-cars', s), city.suburbs[s].get_cars_in(20)) for s in city.suburb_names)),
                  goal=tuple(('<=', ('total-cars', s), 0) for s in city.suburb_names))


def plan():
    planner = DNPlanner(problem)
    planner.solve()

    print(f"\nPriority record:")
    for s, t in city.priority_record:
        print(f"{s}: {t}")

    print(f"------------\n{dict(city.priority_summary)} "
          f"({len(city.priority_record)} changes; total time: {sum(city.priority_summary.values())})")
