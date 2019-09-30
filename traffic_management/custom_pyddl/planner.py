from time import time


class DNPlanner(object):
    """Utility-driven PDDL planner. Heavily inspired by pyddl.planner."""

    def __init__(self, problem, verbose=True):
        self.problem = problem
        self.goal = (problem.goals, problem.num_goals)

        self.current_state = problem.initial_state

        self._total_cost = 0

        self.verbose = verbose

    def next_step(self):
        """Get next generation"""

        node = self.current_state

        # Note: this part comes from pyddl.planner.planner
        # Apply all applicable actions to get successors
        available_actions = set()
        for action in self.problem.grounded_actions:
            if node.is_true(action.preconditions, action.num_preconditions):
                available_actions.add((action, action.evaluate_external()))

        if not available_actions:
            raise RuntimeError("No plan!")

        # select the best node
        best_action, highest_utility = max(available_actions, key=(lambda el: el[1]))

        self.current_state = node.apply(best_action)
        self._total_cost += highest_utility

        # let the external actor apply the effects of the chosen action
        best_action.apply_external()

    def solve(self):
        print("\nStarting the planner")
        start_time = time()

        while not self.current_state.is_true(*self.goal):
            self.next_step()

        plan = self.current_state.plan()

        if self.verbose:
            print(f"\nPlanning completed in {time() - start_time:g} s")
            print(f"Plan length: {len(plan)}")

        return plan
