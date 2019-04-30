import os
from sys import argv
import argparse
from sensors.sensor import sensor
from dispatcher import dispatcher
from utils import get_all_direct_subfolders, get_all_files_recursively, produce_report
from tqdm import tqdm

def structure_the_unstructured(path, verbose):
    d = dispatcher(verbose)
    users = dict()
    user_folders = list(get_all_direct_subfolders(path))
    for user_path in tqdm(user_folders, unit=" users"):
        user = os.path.basename(os.path.normpath(user_path))
        files = list(get_all_files_recursively(user_path))
        users[user] = list(filter(lambda m: len(m), [d.dispatch(f) for f in tqdm(files, unit=" files")]))
    print(users)
    # create acquisition for each user (with subject information from XML)
    # for each device (look for description.xml)
    # TODO: make this operation parallel...?
    
    produce_report(dict(), users) # TODO: include global metrics

def parse_args():
    """Uses argparse module to create a pretty CLI interface that has the -h by default and that helps the user understand the arguments and their usage
    Returns a dict of "argname":"value"
    """
    parser = argparse.ArgumentParser(description="Structuring The UNStructured, a command line tool for mobile sensor data. Network file system files into mongoDB")

    group_settings = parser.add_argument_group('global settings')
    group_settings.add_argument('-p', '--path', help='The source folder where the user folder are contained', required=True)
    group_settings.add_argument('-dsn', '--dataset_name', help='Name of the dataset being processed, default is "Unnamed Dataset"', default="Unnamed Dataset")
    group_settings.add_argument('-v', '--verbose', help='Activate verbose execution', default=False, action="store_true")

    db_settings = parser.add_argument_group('database settings')
    db_settings.add_argument('-mdb', '--mongodb', help='Path to the MongoDB instance, default is "mongodb://localhost:9090/"', default="mongodb://localhost:9090/")
    db_settings.add_argument('-dtn', '--database_name', help='Name of the database inside the MongoDB, default is "demdata_db"', default="demdata_db")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    structure_the_unstructured(args["path"], args["verbose"], args["mongodb"], args["database_name"], args["dataset_name"])
