from sys import argv
import argparse
from sensors.sensor import sensor

def structure_the_unstructured(path):
    print(path)
    s = sensor()
    print(s)

def parse_args():
    parser = argparse.ArgumentParser(description="Structuring The UNStructured, a command line tool for mobile sensor data. Network file system files into mongoDB")
    group_settings = parser.add_argument_group('global settings')
    group_settings.add_argument('-p','--path', help='The source folder where the user folder are contained', required=True)
    return vars(parser.parse_args())



if __name__ == "__main__":
    args = parse_args()
    structure_the_unstructured(args["path"])