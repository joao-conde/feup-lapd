import os
import sys
import glob
import hashlib


def sum(a, b): return a + b


def get_all_files_recursively(root_dir):
    """returns a list of all the files inside the given root_dir, recursively"""
    # TODO: maybe filter for .txt only or to ignore xml
    return filter(os.path.isfile, glob.iglob(root_dir + '**/**', recursive=True))


def hash_file(filename, hasher=hashlib.sha256(), blocksize = 1<<16):
    """Hashes a file and returns its hash, using buffers for better performance"""
    with open(filename, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()