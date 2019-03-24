from .sensor import sensor


class accelerometer(sensor):
    """Sensor for accelerometer data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Accelerometer\.txt"
    columns = ['timestamp', 'x,', 'y,', 'z,', 'precision']
    def __init__(self, file):
        super().__init__(file)
