import os
import sys
from re import search
from tqdm import tqdm
from datetime import datetime
from bson.objectid import ObjectId

from sensors import *


class dispatcher():
    """class used to interpret network file system paths and to dispatch them to the correct sensor parser"""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def get_subclasses(self):
        """Detects direct subclasses of the sensor class and returns them"""
        return sensor.sensor.__subclasses__()

    def dispatch(self, basename, file):
        """given an acquisition filename, assign it to the correct sensor"""
        if basename == "description.xml":
            return {}
        can_receive = list(filter(lambda s: search(s.filter, file), self.get_subclasses()))
        if not len(can_receive):
            if self.verbose:
                print("No dispatcher found for '%s'" % basename, file=sys.stderr)
            return {}
        else:
            s = can_receive[0]
            if len(can_receive) > 1: 
                print("Multiple dispatchers found for '%s', using %s" % (basename, s), file=sys.stderr)
            sensor_parser = s(file)
            metrics = sensor_parser.parse()
            return {"_id": ObjectId(), "sensorType": s.name, "metrics": metrics}  # sensor
