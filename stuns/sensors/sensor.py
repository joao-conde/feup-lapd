import pandas as pd
import json
import time
from pymongo import MongoClient
from utils import hash_file

class sensor:
    """Abstract parent class that defines the method every sensor parser should implement"""

    def __init__(self, file):
        assert self.__class__.filter is not None, "Each sensor should have a static value for 'filter' to identify its files"
        assert self.__class__.columns is not None, "Each sensor should have a static value for 'columns' for the csv-like data columns in the files"
        assert self.__class__.name is not None, "Each sensor should have a static value for 'name' describing the type of sensors they are applied to (sensorType in the database)"
        self.file = file
        self.df = pd.read_csv(self.file, delimiter=",", names=self.__class__.columns)

    def parse(self, acquisition_id, device_id, sensor_id):
        """Main method that handles a sensor file, performs preprocessing operation, extracts metrics and imports the data into the MongoDB instance"""
        self.preprocessing_dataframe()
        
        metrics = self.extract_metrics()

        datapoints = list(json.loads(self.df.T.to_json()).values())
        for i in range(len(datapoints)):
            datapoints[i]["acquisitionId"] = acquisition_id
            datapoints[i]["deviceId"] = device_id
            datapoints[i]["sensorId"] = sensor_id

        return metrics, datapoints

    def preprocessing_dataframe(self):
        """This method can be extended by child classes to do things like bulk conversion of dataframe column from text to date object and other preprocessing operations done before bulk inserting into the database"""
        pass

    def extract_metrics(self, metrics={}):
        """Extract metrics specific to this datafile. Can be extended by child classes that call it for the default metrics"""
        metrics["filename"] = self.file
        metrics["structured_at"] = time.time()
        metrics["rows"] = len(self.df)
        metrics["hash"] = hash_file(self.file)
        return metrics