from .sensor import sensor
import pandas as pd
import json


class accelerometer(sensor):
    """Sensor for accelerometer data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Accelerometer\.txt"
    columns = ['timestamp', 'x,', 'y,', 'z,', 'precision']
    name = "ACCELEROMETER"

    def __init__(self, file):
        super().__init__(file)

    # def preprocessing_dataframe(self):
    #     self.df["timestamp"] = pd.to_datetime(self.df["timestamp"], unit="ms")
