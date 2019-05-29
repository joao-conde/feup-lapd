import os
import sys
import glob
import datetime
import hashlib
import zipfile
from jinja2 import Environment, PackageLoader, select_autoescape


def get_all_direct_subfolders(root_dir):
    """returns a generator of all the direct subfolders of a root dir"""
    def dirname(d): return os.path.basename(os.path.normpath(d)
                                            ), d  # returns the individual folder name, path
    return map(dirname, filter(os.path.isdir, [os.path.join(root_dir, f) for f in os.listdir(root_dir)]))


def get_all_files_recursively(root_dir):
    """returns a generator of all the files inside the given root_dir, recursively"""
    def filename(f): return os.path.normpath(f).split(os.sep)[-1], f  # returns filename without path, path
    return map(filename, filter(os.path.isfile, glob.iglob(root_dir + '**/**', recursive=True)))


def hash_file(filename, hasher=hashlib.sha256(), blocksize=1 << 16):
    """returns a file's hash, uses buffers for better performance"""
    with open(filename, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()


def etree_to_dict(t):
    """returns a python dict corresponding to a parsed etree (xml)"""
    d = {}
    children = list(map(etree_to_dict, t.getchildren()))
    if children:
        d[t.tag] = children
    d.update((k, v) for k, v in t.attrib.items())
    if t.text:
        d['text'] = t.text
    return d


def produce_report(execution_metrics, users):
    """apply a Jinja2 template with the data so as to produce the execution report"""
    env = Environment(
        loader=PackageLoader('stuns', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    # Dark magic from https://stackoverflow.com/questions/5208252/ziplist1-list2-in-jinja2
    env.globals.update(zip=zip)
    template = env.get_template("report.html")

    with open("report.html", "w", encoding="utf-8") as out:
        out.write(template.render(
            date=datetime.datetime.now().strftime("%B %d, %Y %H:%M"),
            execution_metrics=execution_metrics,
            users=users
        ))


def zip_dataset(path, zip_name):
    """zips a dataset folder in the same path"""
    ziph = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
    ziph.close()


def get_dataset_hash(path):
    """returns a dataset hash, created from hashing a zipped version of that dataset"""
    temp_zip_name = "temp.zip"
    zip_dataset(path, temp_zip_name)
    ds_hash = hash_file(temp_zip_name)
    os.remove(temp_zip_name)
    return ds_hash
