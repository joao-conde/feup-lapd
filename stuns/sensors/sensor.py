import pandas as pd
import pymongo


class sensor:
    """Abstract parent class that defines the method every sensor parser should implement"""

    def __init__(self, file, details):
        assert self.__class__.filter is not None, "Each sensor should have a static value for 'filter' to identify its files"
        assert self.__class__.columns is not None, "Each sensor should have a static value for 'columns' for the csv-like data columns in the files"
        self.file = file
        self.details = details
        self.df = pd.read_csv(self.file, delimiter=",", names=self.__class__.columns)

    def parse(self):
        self.preprocessing_dataframe()
        list(map(self.parse_line, self.df.iterrows()))
        # with MongoClient('mongodb://localhost:27017/') as client:
        # db = client["database_name"]
        # collection = db["collection_name"]
        # collection.insert_many(map(self.parse_line, df.iterrows()))

    def preprocessing_dataframe(self):
        """This method can be extended by child classes to do things like bulk conversion of dataframe column from text to date object and other preprocessing operations done before bulk inserting into the database"""
        pass

    def parse_line(index, row):
        """Should convert a row into a dict for insertion in MongoDB"""
        print(row)
        exit()
