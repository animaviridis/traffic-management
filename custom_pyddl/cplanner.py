from time import time


class DNPlanner(object):
    """Utility-driven PDDL planner. Heavily inspired by pyddl.planner."""

    def __init__(self, problem, cost_evaluator=None, verbose=True):
        self.problem = problem
        self.goal = (problem.goals, problem.num_goals)

        self.current_state = problem.initial_state

        self._cost_evaluator = cost_evaluator if cost_evaluator is not None else lambda *args: 0  # TODO
        self._total_cost = 0

        self.verbose = verbose

    def next_step(self):
        """Get next generation"""

        node = self.current_state

        # Note: this part comes from pyddl.planner.planner
        # Apply all applicable actions to get successors
        successors = set()
        for action in self.problem.grounded_actions:
            if node.is_true(action.preconditions, action.num_preconditions):
                action_cost = self._cost_evaluator(*action.sig)
                successors.add((node.apply(action), action_cost))

        if not successors:
            raise RuntimeError("No plan!")

        # select the best node
        best = sorted(successors, key=(lambda el: el[1]))
        self.current_state = best[0]
        self._total_cost += best[1]

    def solve(self):
        start_time = time()

        while not self.current_state.is_true(self.goal):
            self.next_step()

        plan = self.current_state.plan()

        if self.verbose:
            print(f"Planning completed in {time() - start_time:g} s")
            print(f"Plan length: {len(plan)}")
            print(f"Total cost: {self._total_cost:g}")

        return plan
