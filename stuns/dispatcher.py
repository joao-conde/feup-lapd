import os
import sys
from re import search
from datetime import datetime
from uuid import uuid4

from sensors import *


class dispatcher():
    """class used to interpret network file system paths and to dispatch them to the correct sensor parser"""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def get_subclasses(self):
        """Detects direct subclasses of the sensor class and returns them"""
        return sensor.sensor.__subclasses__()

    def dispatch(self, basename, file, acq_id, dev_id, user, metrics_args):
        """given an acquisition filename, assign it to the correct sensor"""
        if basename == "description.xml":
            return {}, {}
        user_context = "[user: %s]" % user
        can_receive = list(filter(lambda s: search(s.filter, file), self.get_subclasses()))
        if not len(can_receive):
            if self.verbose:
                print(user_context, "No dispatcher found for '%s'" % basename, file=sys.stderr)
            return {}, {}
        else:
            s = can_receive[0]
            if self.verbose:
                if len(can_receive) > 1:
                    print(user_context, "Multiple dispatchers found for '%s', using first: %s" % (basename, s), file=sys.stderr)
                else:
                    print(user_context, "Dispatcher found for %s: %s" % (basename, s))

            sensor_id = uuid4()
            sensor_parser = s(file, metrics_args)
            metrics, datapoints = sensor_parser.parse(acq_id, dev_id, sensor_id)
            return {"_id": sensor_id, "sensorType": s.name, "metrics": metrics}, datapoints  # sensor
