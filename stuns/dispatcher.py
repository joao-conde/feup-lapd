import os, sys
from sensors import *
from sensors.sensor import sensor  # avoidable if sensor.sensor is used
from re import search
from datetime import datetime


class dispatcher():
    """class used to interpret network file system paths and to dispatch them to the correct sensor parser"""

    def get_subclasses(self):
        """Detects direct subclasses of the sensor class and returns them"""
        return sensor.__subclasses__()

    def get_file_details(self, file):
        """Given a file path, extract the information inherent to the folder structure into a dictionary"""
        parts = os.path.normpath(file).split(os.sep)
        date = datetime.strptime(parts[5], '%Y-%m-%d_%H-%M-%S')
        return {
            "username": parts[1],  # user01
            "source":   parts[2],  # Protocol
            "location": parts[3],  # Right Pocket
            "device":   parts[4],  # IoTip_Active
            "date":     date      # date time object
        }

    def dispatch(self, file):
        """given an acquisition filename, assign it to the correct sensor"""
        basename = os.path.normpath(file).split(os.sep)[-1]
        can_receive = list(filter(lambda s: search(s.filter, file), self.get_subclasses()))
        if not len(can_receive):
            pass
            print("No dispatcher found for '%s'" % basename, file=sys.stderr)
        elif len(can_receive) > 1:
            pass
            print("Multiple dispatchers found for '%s'. Skipping..." % basename, file=sys.stderr)
        else:
            # print("Dispatching '%s' to %s" % (basename, can_receive[0].__name__))
            sensor_parser = can_receive[0](file, self.get_file_details(file))
            metrics = sensor_parser.parse()
