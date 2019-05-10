from .sensor import sensor
import pandas as pd


class gyroscope(sensor):
    """Sensor for gyroscope data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Gyroscope\.txt"
    columns = ['timestamp', 'x', 'y', 'z', 'precision']
    name = "GYROSCOPE"
    inercial = True

    def __init__(self, file):
        super().__init__(file)

    # def preprocessing_dataframe(self):
    #     self.df["timestamp"] = pd.to_datetime(self.df["timestamp"], unit="ms")
