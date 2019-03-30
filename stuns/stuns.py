from sys import argv
import argparse
from sensors.sensor import sensor
from dispatcher import dispatcher
from utils import get_all_files_recursively
from tqdm import tqdm

def structure_the_unstructured(path):
    d = dispatcher()
    files = list(get_all_files_recursively(path)) # convert to list for to tqdm
    # TODO: make this operation parallel... how will the progress bar change with that
    for f in tqdm(files, unit=" files"): # apply progress bar
        d.dispatch(f)


def parse_args():
    """Uses argparse module to create a pretty CLI interface that has the -h by default and that helps the user understand the arguments and their usage
    Returns a dict of "argname":"value"
    """
    parser = argparse.ArgumentParser(description="Structuring The UNStructured, a command line tool for mobile sensor data. Network file system files into mongoDB")
    group_settings = parser.add_argument_group('global settings')
    group_settings.add_argument('-p', '--path', help='The source folder where the user folder are contained', required=True)
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    structure_the_unstructured(args["path"])
