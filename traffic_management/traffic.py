from argparse import ArgumentParser


class TrafficProperties(object):
    FLOW_FACTOR = 0.05/60

    def __init__(self, junction_flow=200, wait_factor=0.1, base_time=1, ext_time=0.5, acc_time=0.5):
        self.junction_flow = junction_flow
        self.wait_factor = wait_factor  # 'frustration factor' due to waiting

        # traffic lights timing settings
        self.base_time = base_time  # minimal priority duration - 1 minute

        if ext_time > self.base_time:
            raise ValueError("Extension time should not be longer than base time")

        self.ext_time = ext_time  # priority extension time

        if acc_time > self.base_time:
            raise ValueError("Base time cannot be smaller than acceleration time")
        self.acc_time = acc_time  # time before reaching the nominal junction flow

    @staticmethod
    def from_parser(parsed_args):
        """Static constructor for a TrafficProperties object."""

        return TrafficProperties(junction_flow=parsed_args.junction_flow,
                                 wait_factor=parsed_args.wait_factor,
                                 base_time=parsed_args.base_time,
                                 ext_time=parsed_args.base_time,
                                 acc_time=parsed_args.acc_time)

    @staticmethod
    def define_parser():
        parser = ArgumentParser(description="TrafficProperties argument parser")
        parser.add_argument('--junction-flow', default=200, type=float,
                            help="Flow through the junction [cars/minute].")
        parser.add_argument('--wait-factor', default=0.01, type=float,
                            help="A.k.a. frustration factor. Scaling factor for accumulated waiting time "
                                 "in utility function; reflects drivers' frustration from waiting [1/min].")
        parser.add_argument('--base-time', default=1, type=float,
                            help="Minimal (base) duration of priority [min].")
        parser.add_argument('--ext-time', default=0.5, type=float,
                            help="Priority extension time; can be applied any times for given prioritised area [min].")
        parser.add_argument('--acc-time', default=0.5, type=float,
                            help="Time needed to reach the nominal junction flow after switching priority.")

