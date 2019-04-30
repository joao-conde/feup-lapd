import os
import sys
from tqdm import tqdm
from re import search
from datetime import datetime
from sensors import *


class dispatcher():
    """class used to interpret network file system paths and to dispatch them to the correct sensor parser"""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def get_subclasses(self):
        """Detects direct subclasses of the sensor class and returns them"""
        return sensor.sensor.__subclasses__()

    def get_file_details(self, file):
        """Given a file path, extract the information inherent to the folder structure into a dictionary"""
        parts = os.path.normpath(file).split(os.sep)
        date = datetime.strptime(parts[5], '%Y-%m-%d_%H-%M-%S')
        return {
            "username": parts[1],  # user01
            "source": parts[2],  # Protocol
            "acquisition": parts[3],  # Right Pocket
            "device": parts[4],  # IoTip_Active
            "recorded_at": datetime.timestamp(date)       # date time object
        }

    def dispatch(self, basename, file):
        """given an acquisition filename, assign it to the correct sensor"""
        metrics = dict()
        if basename == "description.xml": return metrics
        can_receive = list(filter(lambda s: search(s.filter, file), self.get_subclasses()))
        if not len(can_receive):
            if self.verbose:
                print("No dispatcher found for '%s'" % basename, file=sys.stderr)
        else:
            # TODO: decide if this is necessary: can there be more than one dispatcher for each file?
            for s in tqdm(can_receive):
                sensor_parser = s(file, self.get_file_details(file))
                metrics = sensor_parser.parse(metrics)
        return metrics
