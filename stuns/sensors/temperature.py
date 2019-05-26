from .sensor import sensor
import pandas as pd


class temperature(sensor):
    """Sensor for temperature data, structure is `timestamp, temperature, precision`"""
    filter = ".*Temperature\.txt"
    columns = ['timestamp', 'temperature', 'precision']
    name = "TEMPERATURE"
    inercial = False

    def __init__(self, file, metrics_args):
        super().__init__(file, metrics_args)

    
    def extract_metrics(self, metrics={}):
        metrics = super().extract_metrics(metrics)
        metrics["temperature"] = self.column_metrics("temperature")
        return metrics
