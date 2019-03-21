from sensor import sensor


class accelerometer(sensor):
    """Sensor for accelerometer data, structure is `timestamp, x, y, z, precision`"""
    def __init__(self):
        super().__init__()
