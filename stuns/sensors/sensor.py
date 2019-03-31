import pandas as pd
import pymongo
import json
import time
from utils import hash_file

class sensor:
    """Abstract parent class that defines the method every sensor parser should implement"""

    def __init__(self, file, details):
        assert self.__class__.filter is not None, "Each sensor should have a static value for 'filter' to identify its files"
        assert self.__class__.columns is not None, "Each sensor should have a static value for 'columns' for the csv-like data columns in the files"
        self.file = file
        self.details = details
        self.df = pd.read_csv(self.file, delimiter=",", names=self.__class__.columns)

    def parse(self, old_metrics=None):
        """Main method that handles a sensor file, performs preprocessing operation, extracts metrics and imports the data into the MongoDB instance"""
        self.preprocessing_dataframe()
        # self.df.apply(self.process_row, axis=1)
        metrics = self.extract_metrics(old_metrics)
        self.insert_into_db()
        return metrics

    def preprocessing_dataframe(self):
        """This method can be extended by child classes to do things like bulk conversion of dataframe column from text to date object and other preprocessing operations done before bulk inserting into the database"""
        pass

    def extract_metrics(self, _metrics=None):
        """Extract metrics specific to this datafile. Can be extended by child classes that call it for the default metrics"""
        metrics = _metrics if _metrics else dict()
        metrics["filename"] = self.file
        metrics["structured_at"] = time.time()
        metrics["rows"] = len(self.df)
        metrics["hash"] = hash_file(self.file)
        metrics.update(self.details)
        return metrics

    def insert_into_db(self):
        """Performs database connection operations and inserts the dataframe data into it"""
        # with MongoClient('mongodb://localhost:27017/') as client:
        # db = client["database_name"]
        # collection = db["collection_name"]
        # collection.insert_many(map(self.row_to_dict, self.df.iterrows()))
        # alternative that generates the whole JSON
        records = json.loads(self.df.T.to_json()).values()
        # collection.insert(records)
        pass
