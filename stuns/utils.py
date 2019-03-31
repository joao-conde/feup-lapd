import os
import sys
import glob
import hashlib
from jinja2 import Environment, PackageLoader, select_autoescape


def sum(a, b): return a + b


def get_all_direct_subfolders(root_dir):
    """returns a generator of all the direct subfolders of a root dir"""
    return filter(os.path.isdir, [os.path.join(root_dir, f) for f in os.listdir(root_dir)])


def get_all_files_recursively(root_dir):
    """returns a generator of all the files inside the given root_dir, recursively"""
    # TODO: maybe filter for .txt only or to ignore xml
    return filter(os.path.isfile, glob.iglob(root_dir + '**/**', recursive=True))


def hash_file(filename, hasher=hashlib.sha256(), blocksize=1 << 16):
    """Hashes a file and returns its hash, using buffers for better performance"""
    with open(filename, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()


def produce_report(execution_metrics, users):
    """Apply a Jinja2 template with the data so as to produce the execution report"""
    env = Environment(
        loader=PackageLoader('stuns', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template("report.html")
    with open("report.html", "w", encoding="utf-8") as out:
        out.write(template.render(date="31 de Março", my_list=[1, 2, 3, 4], execution_metrics=execution_metrics, users=users))
