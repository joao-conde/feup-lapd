from .sensor import sensor
import pandas as pd


class magnetometer(sensor):
    """Sensor for magnetometer data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Magnetometer\.txt"
    columns = ['timestamp', 'x', 'y', 'z', 'precision']
    name = "MAGNETOMETER"
    inercial = True

    def __init__(self, file, metrics_args):
        super().__init__(file, metrics_args)
