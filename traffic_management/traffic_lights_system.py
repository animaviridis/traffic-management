from pyddl import Domain, Problem, Action, neg, planner
from traffic_management.city import define_city
from traffic_management.traffic import TrafficProperties


city = define_city()


def tnc(suburb):
    return city.suburbs[suburb].get_inflow(5)  # TODO: time window from arg parser


a1 = Action('switch-priority',
            parameters=(('suburb', 'S1'), ('suburb', 'S2')),
            preconditions=(('prioritised', 'S1'),),  # TODO: S1 != S2 - possible?
            effects=(neg(('prioritised', 'S1')),
                     ('prioritised', 'S2'),
                     ('-=', ('total-cars', 'S2'), TrafficProperties.get_base_outflow()))
            )

a2 = Action('extend-priority',
            parameters=(('suburb', 'S'),),
            preconditions=(('prioritised', 'S'),),
            effects=(('-=', ('total-cars', 'S'), TrafficProperties.get_ext_outflow()),)
            )


domain = Domain((a1, a2))


problem = Problem(domain, {'suburb': tuple(city.suburb_names)},
                  init=(('prioritised', 'A'),
                        *tuple(('=', ('total-cars', s), tnc(s)) for s in city.suburb_names)),
                  goal=tuple(('<=', ('total-cars', s), 0) for s in city.suburb_names))


