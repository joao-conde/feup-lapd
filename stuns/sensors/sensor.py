import pandas as pd
import json
import time
from pymongo import MongoClient
from utils import hash_file
import pandas_profiling as pp


class sensor:
    """Abstract parent class that defines the method every sensor parser should implement"""

    def __init__(self, file, metrics_args):
        assert self.__class__.filter is not None, "Each sensor should have a static value for 'filter' to identify its files"
        assert self.__class__.columns is not None, "Each sensor should have a static value for 'columns' for the csv-like data columns in the files"
        assert self.__class__.name is not None, "Each sensor should have a static value for 'name' describing the type of sensors they are applied to (sensorType in the database)"
        assert self.__class__.inercial is not None, "Each sensor should have a static boolean value for 'inercial' describing it as having x,y,z information or not"
        self.file = file
        self.metrics_args = metrics_args
        self.df = pd.read_csv(self.file, delimiter=",", names=self.__class__.columns, header=None)

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

    def column_metrics(self, col_name):
        col = self.df[col_name]
        mi, ma = col.min(), col.max()
        res = {
            "range": str(abs(ma - mi)),
            "missing": str(col.isnull().sum())
        }
        # describe includes: count,mean,std,min,25%,50%,75%,max
        for k, v in col.describe().iteritems():
            res[k] = str(v)
        return res

    def file_metrics(self, metrics={}):
        metrics["filename"] = self.file
        metrics["structured_at"] = time.time()
        metrics["rows"] = len(self.df)
        metrics["hash"] = hash_file(self.file)
        return metrics

    def extract_metrics(self, metrics={}):
        """Extract metrics specific to this datafile. Can be extended by child classes that call it for the default metrics"""
        # global file metrics
        metrics = self.file_metrics(metrics)

        # inercial
        if self.__class__.inercial:
            metrics["x"] = self.column_metrics("x")
            metrics["y"] = self.column_metrics("y")
            metrics["z"] = self.column_metrics("z")

        # global
        metrics["precision"] = self.column_metrics("precision")
        # minimum threshold for precision
        metrics["precision"]["below_min_precision"] = str((self.df["precision"] < float(self.metrics_args["min_precision"])).sum())

        filename = "report/%s.html" % metrics["hash"]
        if self.metrics_args["pandas_profiling"]:
            profile = pp.ProfileReport(self.df)
            profile.to_file(outputfile=filename)
        else:
            with open(filename, "w") as out:
                out.write("To see these reports activate Pandas Profiling argument (-pp) in stuns")

        return metrics
