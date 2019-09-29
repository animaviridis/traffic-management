from argparse import ArgumentParser
import datetime as dt
import numpy as np

_working_days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri')
_weekend = ('Sat', 'Sun')
_weekdays = {**{day: 1 for day in _working_days},
             **{calm_day: 0 for calm_day in ('Sat', 'Sun')}}

_hour_limits = [dt.time(hour=h) for h in (7, 10, 16, 19)]
_periods = {k: k%2 for k in range(5)}


class TrafficSchedule(object):
    WEEKDAYS = _weekdays
    HOURS = _hour_limits
    PERIODS = _periods

    def __init__(self, weekday: str, hour: int, **kwargs):
        self._weekday = ''
        self._set_weekday(weekday)

        self._time = dt.time(hour=hour, **kwargs)
        self._busy = self.is_busy()

    def set_time(self, **kwargs):
        self._time = dt.time(**kwargs)
        self._busy = self.is_busy()

    @property
    def weekday(self):
        return self._weekday

    @weekday.setter
    def weekday(self, weekday: str):
        self._set_weekday(weekday)
        self._busy = self.is_busy()

    @property
    def time(self):
        return self._time

    def _set_weekday(self, weekday: str):
        if weekday[:3] not in self.WEEKDAYS.keys():
            raise ValueError(f"Weekday {weekday} not recognised")
        self._weekday = weekday[:3]

    def is_busy(self):
        if not self.WEEKDAYS[self.weekday]:
            return False

        period = np.searchsorted(self.HOURS, self.time)
        return bool(self.PERIODS[period])

    @property
    def busy(self):
        return self._busy

    @staticmethod
    def define_parser():
        parser = ArgumentParser(description="Traffic Schedule argument parser", add_help=False)
        parser.add_argument('--weekday', type=str, choices=list(TrafficSchedule.WEEKDAYS.keys()),
                            help="Day of the week to run the analysis for")
        parser.add_argument('--hour', type=int, choices=list(range(24)),
                            help="Hour during the day to run the analysis for (24h day format)")
        return parser


class TrafficProperties(object):
    FLOW_FACTOR = 0.05/60

    def __init__(self, junction_flow=200, wait_factor=0.1, base_time=1, ext_time=0.5, acc_time=0.5,
                 **kwargs):

        self.schedule = TrafficSchedule(**kwargs)

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
                                 acc_time=parsed_args.acc_time,
                                 weekday=parsed_args.weekday,
                                 hour=parsed_args.hour)

    @staticmethod
    def define_parser():
        parser = ArgumentParser(description="TrafficProperties argument parser", add_help=False,
                                parents=[TrafficSchedule.define_parser()])
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

        return parser

