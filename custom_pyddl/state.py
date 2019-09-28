import pyddl


class State(pyddl.State):
    def apply(self, action, monotone=False):
        """Note: this method comes mostly from pyddl.State.apply; it is overwritten to support functional numerical
        predicate evaluation at application of the given state - to account for dynamics of the external model.

        Apply the action to this state to produce a new state.
        If monotone, ignore the delete list (for A* heuristic)
        """

        new_preds = set(self.predicates)
        new_preds |= set(action.add_effects)
        if not monotone:
            new_preds -= set(action.del_effects)
        new_functions = dict()
        new_functions.update(self.functions)
        for function, (value_sign, value_func, value_args) in action.num_effects:
            new_functions[function] += value_sign*value_func(action.name, *value_args)  # evaluate the value function

        return State(new_preds, new_functions, self.cost + action.evaluate_external(), (self, action))

