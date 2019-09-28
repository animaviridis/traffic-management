import pyddl
from custom_pyddl.state import State


class Problem(pyddl.Problem):
    """Note: this object is an extension of pyddl.Problem, made for handling of the functional numerical effects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # use the subclassed State instead of pyddl.State
        self.initial_state = State(self.initial_state.predicates, self.initial_state.f_dict)
