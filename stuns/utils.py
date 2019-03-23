import os
import sys
import glob


def sum(a, b): return a + b

def get_all_files_recursively(root_dir):
    """returns a list of all the files inside the given root_dir, recursively"""
    # TODO: maybe filter for .txt only or to ignore xml
    return filter(os.path.isfile, glob.iglob(root_dir + '**/**', recursive=True))
