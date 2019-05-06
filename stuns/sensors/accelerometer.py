from .sensor import sensor
import pandas as pd
import json


class accelerometer(sensor):
    """Sensor for accelerometer data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Accelerometer\.txt"
    columns = ['timestamp', 'x', 'y', 'z', 'precision']
    name = "ACCELEROMETER"
    inercial = True

    def __init__(self, file):
        super().__init__(file)

    def extract_metrics(self, metrics={}):
        metrics = super().extract_metrics(metrics)
        
        return metrics

