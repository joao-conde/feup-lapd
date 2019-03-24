from .sensor import sensor


class gyroscope(sensor):
    """Sensor for gyroscope data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Gyroscope\.txt"
    columns = {'timestamp', 'x,', 'y,', 'z,', 'precision'}
    def __init__(self, file):
        super().__init__(file)
    