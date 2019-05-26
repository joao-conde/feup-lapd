from .sensor import sensor
import pandas as pd


class gyroscope(sensor):
    """Sensor for gyroscope data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Gyroscope\.txt"
    columns = ['timestamp', 'x', 'y', 'z', 'precision']
    name = "GYROSCOPE"
    inercial = True

    def __init__(self, file, metrics_args):
        super().__init__(file, metrics_args)
