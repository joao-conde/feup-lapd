from .sensor import sensor
import pandas as pd
import json


class all(sensor):
    """Abstract Sensor for the "all.txt" file to perform analysis on the time aggregated time series"""
    filter = ".*all\.txt"
    columns = ['sensor', 'timestamp', '_1', '_2', '_3', '_4']
    name = "ALL"
    inercial = True

    def __init__(self, file, metrics_args):
        super().__init__(file, metrics_args)

    def parse_datapoints(self, acquisition_id, device_id, sensor_id):
        return []

    def extract_metrics(self, metrics={}):
        # global file metrics
        metrics = self.file_metrics(metrics)

        return metrics
