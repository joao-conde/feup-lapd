import os, shutil
from sys import argv
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET
from pymongo import MongoClient
from threading import Thread
import multiprocessing

from sensors.sensor import sensor
from dispatcher import dispatcher
from utils import get_all_direct_subfolders, get_all_files_recursively, produce_report, etree_to_dict, get_dataset_hash

from bson.binary import JAVA_LEGACY
from bson.codec_options import CodecOptions
from uuid import uuid4

def get_mongo_client(mongo, database_name):
    client = MongoClient(mongo)
    db = client.get_database(database_name, CodecOptions(uuid_representation=JAVA_LEGACY))
    c_ds = db["datasets"]  # create dataset instance and get Id
    return client, db, c_ds


def structure_the_unstructured(path, verbose, mongo, database_name, dataset_name, skip_duplicate, metrics_args):
    # get db instace
    client, db, c_ds = get_mongo_client(mongo, database_name)

    if verbose: print("Calculating Dataset hash")
    ds_hash = get_dataset_hash(path)

    if not skip_duplicate: 
        if verbose:
            print("Checking for repeated imports...")
            
        identical_ds_cnt = c_ds.count_documents({"hash": ds_hash})

        if identical_ds_cnt != 0:
            opt = input("\nDataset '%s' was imported %s time(s) already.\nDo you wish to continue and import it again? (y/n) " % (path, identical_ds_cnt))
            while True:
                if opt == "Y" or opt == "y": 
                    print("\nProceeding with import...\n")
                    break
                if opt == "N" or opt == "n": 
                    print("\nAborting import...\n")
                    return    
                opt = input("\nInvalid option. Options are:\n\t- Confirm dataset import - [Y/y]\n\t- Cancel dataset import - [N/n]\nOption: ")

    create_report_folder()
    # TODO remove ds_id (dataset_id) if it remains unused by the end of the project
    ds_id = c_ds.insert({"_id": uuid4(), "className": "pt.fraunhofer.demdatarepository.model.dataset.Dataset", "name": dataset_name, "type": "Dataset", "hash": ds_hash})
    client.close()

    d = dispatcher(verbose)  # create a dispatcher instance
    users = {}
    global_metrics = {}
    # multiprocessing
    pool = multiprocessing.Pool()
    processes = []
    for user, uf in get_all_direct_subfolders(path):
        processes.append(pool.apply_async(process_user, args=([d, user, uf, verbose, metrics_args, mongo, database_name])))
    for p in processes:  # before producing the report, wait for workers
        user, result, subject = p.get()
        users[user] = result
        global_metrics['total_subjects'] = global_metrics.get('total_subjects', 0) + 1
        global_metrics['male_subjects'] = global_metrics.get('male_subjects', 0) + 1 if subject.get('gender', None) == 'Male' else 0
        global_metrics['female_subjects'] = global_metrics.get('total_subjects', 0) + 1 if subject.get('gender', None) == 'Female' else 0
        global_metrics['max_age'] = max(global_metrics.get('max_age', 0), float(subject.get('age', 0)))
        global_metrics['min_age'] = min(global_metrics.get('min_age', 0), float(subject.get('age', 0)))
        global_metrics['avg_age'] = (global_metrics.get('avg_age', 0) * len(processes) + float(subject.get('age', 0))) / len(processes)
        global_metrics['max_height'] = max(global_metrics.get('max_height', 0), float(subject.get('height', 0)))
        global_metrics['min_height'] = min(global_metrics.get('min_height', 0), float(subject.get('height', 0)))
        global_metrics['avg_height'] = (global_metrics.get('avg_height', 0) * len(processes) + float(subject.get('height', 0))) / len(processes)

    produce_report(global_metrics, users)


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

    acq_id = c_acq.insert({"_id": uuid4(), "className": "pt.fraunhofer.demdatarepository.model.dataset.Acquisition", "creationTimestamp": int(
        datetime.now().timestamp()), "timeUnit": "SECONDS", "type": "Acquisition"})

    c_samples = db["samples"]
    subject = None
    result = []
    for protocol, pf in get_all_direct_subfolders(uf):
        for location, lf in get_all_direct_subfolders(pf):
            for device_str, df in get_all_direct_subfolders(lf):
                sensors = []
                dev_id = uuid4()
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
                                if len(datapoints):
                                    c_samples.insert([{"_id": uuid4(), **datapoint} for datapoint in datapoints])
                if len(sensors):
                    device["sensors"] = sensors
                c_acq.update_one({"_id": acq_id}, {"$push": {"devices": device}})
                result += [device, sensors]
    if subject:
        c_acq.update_one({"_id": acq_id}, {"$set": {"subject": subject}})
    client.close()
    return user, result, subject


def parse_args():
    """Uses argparse module to create a pretty CLI interface that has the -h by default and that helps the user understand the arguments and their usage
    Returns a dict of "argname":"value"
    """
    parser = argparse.ArgumentParser(
        description="Structuring The UNStructured, a command line tool for mobile sensor data. Network file system files into mongoDB")

    group_settings = parser.add_argument_group('global settings')
    group_settings.add_argument('-p', '--path', help='The source folder where the user folder are contained', required=True)
    group_settings.add_argument('-dsn', '--dataset_name', help='Name of the dataset being processed, default is "Unnamed Dataset"', default="Unnamed Dataset")
    group_settings.add_argument('-sd', '--skip_duplicate', help='If used there won\'t be a check for duplicate dataset insertion', default=False, action="store_true")
    group_settings.add_argument('-v', '--verbose', help='Activate verbose execution', default=False, action="store_true")

    db_settings = parser.add_argument_group('database settings')
    db_settings.add_argument(
        '-mdb', '--mongodb', help='Path to the MongoDB instance, default is "mongodb://localhost:9090/"', default="mongodb://localhost:9090/")
    db_settings.add_argument('-dtn', '--database_name',
                             help='Name of the database inside the MongoDB, default is "demdata_db"', default="demdata_db")

    metrics_settings = parser.add_argument_group('metrics settings')
    metrics_settings.add_argument("-mp", "--min_precision", help="The minimum acceptable value for precision, datapoints below this threshold are counted", default=0)
    metrics_settings.add_argument("-td", "--timestamp_diff_to_second", help="What is the magnitude of seconds in the timestamp values, eg: 3 means that the 3rd digit from the right is the seconds digit. This is used for the sample frequency calculation.", default=8)
    metrics_settings.add_argument('-pp', '--pandas_profiling', help='User pandas profiling (requires `sudo apt-get install python3-tk`) and may crash on some machines, but yields more informative html reports', default=False, action="store_true")

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    metrics_args = {
        "min_precision": args["min_precision"],
        "pandas_profiling": args["pandas_profiling"],
        "timestamp_diff_to_second": args["timestamp_diff_to_second"]
    }
    structure_the_unstructured(args["path"], args["verbose"], args["mongodb"], args["database_name"], args["dataset_name"], args["skip_duplicate"], metrics_args)
