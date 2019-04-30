import os
from sys import argv
import argparse
from datetime import datetime
from collections import defaultdict
import xml.etree.ElementTree as ET
from tqdm import tqdm
from pymongo import MongoClient
from bson.objectid import ObjectId

from sensors.sensor import sensor
from dispatcher import dispatcher
from utils import get_all_direct_subfolders, get_all_files_recursively, produce_report, etree_to_dict


def structure_the_unstructured(path, verbose, mongo, database_name, dataset_name):
    # TODO: avoid duplicate, perhaps with hash in dataset document
    with MongoClient(mongo) as client:
        db = client[database_name]
        # create dataset instance and get Id
        c_ds = db["datasets"]
        ds_id = c_ds.insert({"className": "pt.fraunhofer.demdatarepository.model.dataset.Dataset", "name": dataset_name, "type": "Dataset", "hash": "TODO"})

        users = defaultdict(list)
        d = dispatcher(verbose)  # create a dispatcher instance

        for user, uf in get_all_direct_subfolders(path):
            # create acquisition
            c_acq = db["acquisitions"]
            acq_id = c_acq.insert({"className": "pt.fraunhofer.demdatarepository.model.dataset.Acquisition", "creationTimestamp": int(datetime.now().timestamp()), "timeUnit": "SECONDS", "type": "Acquisition"})

            subject = None
            for protocol, pf in get_all_direct_subfolders(uf):
                for location, lf in get_all_direct_subfolders(pf):
                    for device_str, df in get_all_direct_subfolders(lf):
                        sensors = []
                        for date_str, dtf in get_all_direct_subfolders(df):
                            date = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')
                            for file, fp in get_all_files_recursively(dtf):
                                if file == "description.xml":
                                    if not subject:
                                        subject = parse_info_xml(fp, "user")
                                    device = parse_info_xml(fp, "phone")
                                    device["type"] = "Device"
                                    device["_id"] = ObjectId()
                                else:
                                    sensor = d.dispatch(file, fp)
                                    if len(sensor): sensors.append(sensor)
                        if len(sensors): device["sensors"] = sensors
                        c_acq.update_one({"_id": acq_id}, {"$push": {"devices": device}})
                        users[user] += (device, sensors)

            # TODO: insert subject into acquisition if != None
            print(subject)
            if subject:
                c_acq.update_one({"_id": acq_id}, {"$set": {"subject": subject}})

    # TODO: make this operation parallel

    # produce_report(dict(), users)  # TODO: include global metrics


def parse_info_xml(filepath, target):
    """return a dict from xml of a given target"""
    root = ET.parse(filepath).getroot()
    return etree_to_dict(root.find(target))


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
