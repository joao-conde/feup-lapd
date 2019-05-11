import os, shutil
from sys import argv
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET
from tqdm import tqdm
from pymongo import MongoClient
from bson.objectid import ObjectId
from threading import Thread
import multiprocessing

from sensors.sensor import sensor
from dispatcher import dispatcher
from utils import get_all_direct_subfolders, get_all_files_recursively, produce_report, etree_to_dict, get_dataset_hash


def get_mongo_client(mongo, database_name):
    client = MongoClient(mongo)
    db = client[database_name]
    c_ds = db["datasets"]  # create dataset instance and get Id
    return client, db, c_ds


def structure_the_unstructured(path, verbose, mongo, database_name, dataset_name, metrics_args):
    # get db instace
    client, db, c_ds = get_mongo_client(mongo, database_name)

    if verbose:
        print("Checking for repeated imports...")
    ds_hash = get_dataset_hash(path)
    identical_ds_cnt = c_ds.count_documents({"hash": ds_hash})

    if identical_ds_cnt != 0:
        opt = input("Dataset '%s' was imported %s time(s) already.\nDo you wish to continue and import it again? (y/n) " % (path, identical_ds_cnt))
        if opt != "Y" and opt != "y":
            return

    create_report_folder()
    # TODO remove ds_id (dataset_id) if it remains unused by the end of the project
    ds_id = c_ds.insert({"className": "pt.fraunhofer.demdatarepository.model.dataset.Dataset",
                         "name": dataset_name, "type": "Dataset", "hash": ds_hash})
    client.close()

    # Start parallel processing
    pool = multiprocessing.Pool()
    processes = []
    d = dispatcher(verbose)  # create a dispatcher instance
    for user, uf in get_all_direct_subfolders(path):
        # process_user(db, users, d, user, uf, verbose, metrics_args, mongo, database_name)
        processes.append(pool.apply_async(process_user, args=([d, user, uf, verbose, metrics_args, mongo, database_name])))
        # p = multiprocessing.Process(target=process_user, args=([users, d, user, uf, verbose, metrics_args, mongo, database_name]))
        # p.start()
        # processes.append(p)
    # final_result = [worker.get() for worker in workers]

    users = {}
    for p in processes:  # before producing the report, wait for workers
        user, result = p.get()
        users[user]= result

    produce_report(dict(), users)  # TODO: include global metrics


def create_report_folder(report_folder="report"):
    if os.path.exists(report_folder):
        shutil.rmtree(report_folder)
    os.mkdir(report_folder)  # for the helper html files


def parse_info_xml(filepath, target):
    """return a dict from xml of a given target"""
    root = ET.parse(filepath).getroot()
    return etree_to_dict(root.find(target))


def process_user(dispatcher, user, uf, verbose, metrics_args, mongo, database_name):
    if verbose:
        print("Processing user: %s" % user)

    client, db, c_ds = get_mongo_client(mongo, database_name)

    c_acq = db["acquisitions"]  # create acquisition

    acq_id = c_acq.insert({"className": "pt.fraunhofer.demdatarepository.model.dataset.Acquisition", "creationTimestamp": int(
        datetime.now().timestamp()), "timeUnit": "SECONDS", "type": "Acquisition"})

    c_samples = db["samples"]
    subject = None
    result = []
    for protocol, pf in get_all_direct_subfolders(uf):
        for location, lf in get_all_direct_subfolders(pf):
            for device_str, df in get_all_direct_subfolders(lf):
                sensors = []
                dev_id = ObjectId()
                for date_str, dtf in get_all_direct_subfolders(df):
                    date = datetime.strptime(
                        date_str, '%Y-%m-%d_%H-%M-%S')
                    for file, fp in get_all_files_recursively(dtf):
                        if file == "description.xml":
                            if not subject:
                                subject = parse_info_xml(fp, "user")
                            device = parse_info_xml(fp, "phone")
                            device["type"] = "Device"
                            device["_id"] = dev_id
                        else:
                            sensor, datapoints = dispatcher.dispatch(file, fp, acq_id, dev_id, user, metrics_args)
                            if len(sensor):
                                sensors.append(sensor)
                                c_samples.insert(datapoints)
                if len(sensors):
                    device["sensors"] = sensors
                c_acq.update_one({"_id": acq_id}, {"$push": {"devices": device}})
                result+= [device, sensors]
    if subject:
        c_acq.update_one({"_id": acq_id}, {"$set": {"subject": subject}})
    client.close()
    return user, result


def parse_args():
    """Uses argparse module to create a pretty CLI interface that has the -h by default and that helps the user understand the arguments and their usage
    Returns a dict of "argname":"value"
    """
    parser = argparse.ArgumentParser(
        description="Structuring The UNStructured, a command line tool for mobile sensor data. Network file system files into mongoDB")

    group_settings = parser.add_argument_group('global settings')
    group_settings.add_argument('-p', '--path', help='The source folder where the user folder are contained', required=True)
    group_settings.add_argument('-dsn', '--dataset_name', help='Name of the dataset being processed, default is "Unnamed Dataset"', default="Unnamed Dataset")
    group_settings.add_argument('-v', '--verbose', help='Activate verbose execution', default=False, action="store_true")

    db_settings = parser.add_argument_group('database settings')
    db_settings.add_argument(
        '-mdb', '--mongodb', help='Path to the MongoDB instance, default is "mongodb://localhost:9090/"', default="mongodb://localhost:9090/")
    db_settings.add_argument('-dtn', '--database_name',
                             help='Name of the database inside the MongoDB, default is "demdata_db"', default="demdata_db")

    metrics_settings = parser.add_argument_group('metrics settings')
    metrics_settings.add_argument("-mp", "--min_precision", help="The minimum acceptable value for precision, datapoints below this threshold are counted", default=0)
    metrics_settings.add_argument('-pp', '--pandas_profiling', help='User pandas profiling (requires `sudo apt-get install python3-tk`) and may crash on some machines, but yields more informative html reports', default=False, action="store_true")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    metrics_args = {
        "min_precision": args["min_precision"],
        "pandas_profiling": args["pandas_profiling"]
    }
    structure_the_unstructured(args["path"], args["verbose"], args["mongodb"], args["database_name"], args["dataset_name"], metrics_args)
