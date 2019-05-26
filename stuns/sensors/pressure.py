from .sensor import sensor
import pandas as pd


class pressure(sensor):
    """Sensor for pressure data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Pressure\.txt"
    columns = ['timestamp', 'pressure', 'precision']
    name = "PRESSURE"
    inercial = False

    def __init__(self, file, metrics_args):
        super().__init__(file, metrics_args)

    
    def extract_metrics(self, metrics={}):
        metrics = super().extract_metrics(metrics)
        metrics["pressure"] = self.column_metrics("pressure")
        return metrics
