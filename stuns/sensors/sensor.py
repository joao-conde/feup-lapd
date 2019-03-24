import pandas as pd

class sensor:
    """Abstract parent class that defines the method every sensor parser should implement"""

    def __init__(self, file, details):
        assert self.__class__.filter is not None, "Each sensor should have a static value for 'filter' to identify its files"
        assert self.__class__.columns is not None, "Each sensor should have a static value for 'columns' for the csv-like data columns in the files"
        self.file = file
        self.details = details
        self.df = pd.read_csv(self.file, delimiter=",",names=self.__class__.columns) #, usecols=self.__class__.columns
        print(self.df.head())
        print(self.df.columns)
