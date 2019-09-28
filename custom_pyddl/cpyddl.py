import pyddl


class Action(pyddl.Action):
    def ground(self, *args):
        return GroundedAction(self, *args)


class GroundedAction(object):
    def __init__(self, action, *args):
        self.name = action.name

        ground = self._grounder(action.arg_names, args)

        # Ground Action Signature
        self.sig = ground((self.name,) + action.arg_names)

        # Ground Preconditions
        self.preconditions = list()
        self.num_preconditions = list()
        self.ground_predicates(action, ground)

        # Ground Effects
        self.add_effects = list()
        self.del_effects = list()
        self.num_effects = list()
        self.ground_effects(action, ground, *args)

    def ground_effects(self, action, ground, *args):
        """Note: this method comes mostly from pyddl._GroundedAction.__init__.
        It is rewritten to change numerical effect values to functions, depending on action's arguments."""

        for effect in action.effects:
            if effect[0] == -1:
                self.del_effects.append(ground(effect[1]))
            elif effect[0] == '+=':
                function = ground(effect[1])
                value = effect[2](action.name, *args)
                self.num_effects.append((function, value))
            elif effect[0] == '-=':
                function = ground(effect[1])
                value = -effect[2](action.name, *args)
                self.num_effects.append((function, value))
            else:
                self.add_effects.append(ground(effect))

    def ground_predicates(self, action, ground):
        """Note: this method comes from pyddl._GroundedAction.__init__"""

        for pre in action.preconditions:
            if pre[0] in pyddl.NUM_OPS:
                operands = [0, 0]
                for i in range(2):
                    if type(pre[i + 1]) == int:
                        operands[i] = pre[i + 1]
                    else:
                        operands[i] = ground(pre[i + 1])
                np = _num_pred(pyddl.NUM_OPS[pre[0]], *operands)
                self.num_preconditions.append(np)
            else:
                self.preconditions.append(ground(pre))

    @staticmethod
    def _grounder(arg_names, args):
        """
        Returns a function for grounding predicates and function symbols

        Note: this method comes entirely from the pyddl module
        """
        namemap = dict()
        for arg_name, arg in zip(arg_names, args):
            namemap[arg_name] = arg

        def _ground_by_names(predicate):
            return predicate[0:1] + tuple(namemap.get(arg, arg) for arg in predicate[1:])

        return _ground_by_names

    def __str__(self):
        """Note: this method is a copy of pyddl._GroundedAction"""

        arglist = ', '.join(map(str, self.sig[1:]))
        return '%s(%s)' % (self.sig[0], arglist)
