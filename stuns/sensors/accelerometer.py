from .sensor import sensor
import pandas as pd
import json

class accelerometer(sensor):
    """Sensor for accelerometer data, structure is `timestamp, x, y, z, precision`"""
    filter = ".*Accelerometer\.txt"
    columns = ['timestamp', 'x,', 'y,', 'z,', 'precision']

    def __init__(self, file, details):
        super().__init__(file, details)
        self.collection = self.db.acquisitions

    
    # def preprocessing_dataframe(self):
    #     self.df["timestamp"] = pd.to_datetime(self.df["timestamp"], unit="ms")

    def insert_into_db(self):
        """Performs database connection operations and inserts the dataframe data into it"""
        # with MongoClient('mongodb://localhost:27017/') as client:
        # db = client["database_name"]
        # collection = db["collection_name"]
        # collection.insert_many(map(self.row_to_dict, self.df.iterrows()))
        # alternative that generates the whole JSON
        records = json.loads(self.df.T.to_json()).values()
        self.collection.insert_many(records)#.inserted_ids #prop that returns unique object IDs of inserted docs (may be useful for "foreign keys")
