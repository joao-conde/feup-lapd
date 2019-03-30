from .sensor import sensor
import pandas as pd

class accelerometer(sensor):
    """Sensor for accelerometer data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Accelerometer\.txt"
    columns = ['timestamp', 'x,', 'y,', 'z,', 'precision']

    def __init__(self, file, details):
        super().__init__(file, details)

    
    # def preprocessing_dataframe(self):
    #     self.df["timestamp"] = pd.to_datetime(self.df["timestamp"], unit="ms")
