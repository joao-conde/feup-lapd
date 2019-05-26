from .sensor import sensor
import pandas as pd


class relative_humidity(sensor):
    """Sensor for relative_humidity data, structure is `timestamp, humidity, precision`"""
    filter = ".*RelativeHumidity\.txt"
    columns = ['timestamp', 'humidity', 'precision']
    name = "RELATIVE_HUMIDITY"
    inercial = False

    def __init__(self, file, metrics_args):
        super().__init__(file, metrics_args)

    
    def extract_metrics(self, metrics={}):
        """Extracts metrics for the relative_humidity sensor
        Appends the metrics to metrics dict with key "humidity" and returns it
        """
        metrics = super().extract_metrics(metrics)
        metrics["humidity"] = self.column_metrics("humidity")
        return metrics
