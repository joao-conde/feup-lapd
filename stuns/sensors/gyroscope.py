from .sensor import sensor


class gyroscope(sensor):
    """Sensor for gyroscope data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Gyroscope\.txt"
    def __init__(self, file):
        super().__init__(file)
