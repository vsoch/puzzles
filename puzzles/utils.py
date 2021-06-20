__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

import fnmatch
import json
import os
import re
import tempfile
from collections import OrderedDict
import sys


def get_installdir():
    """
    get_installdir returns the installation directory of the application
    """
    return os.path.abspath(os.path.dirname(__file__))


def get_temporary_name(prefix=None, ext=None):
    """
    Get a temporary name, can be used for a directory or file.

    Parameters
    ==========
    prefix: if defined, add the prefix after deid
    ext: if defined, return the file extension appended. Do not specify "."
    """
    default_prefix = "puzzles-"
    if prefix:
        default_prefix = "puzzles-%s-" % prefix

    tmpname = os.path.join(
        tempfile.gettempdir(),
        "%s%s" % (default_prefix, next(tempfile._get_candidate_names())),
    )
    if ext:
        tmpname = "%s.%s" % (tmpname, ext)
    return tmpname


################################################################################
## FILE OPERATIONS #############################################################
################################################################################


def copyfile(source, destination, force=True):
    """
    Copy a file from a source to its destination.
    """
    # Case 1: It's already there, we aren't replacing it :)
    if source == destination and force is False:
        return destination

    # Case 2: It's already there, we ARE replacing it :)
    if os.path.exists(destination) and force is True:
        os.remove(destination)

    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode="w"):
    """
    Write content to file.
    """
    with open(filename, mode) as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode="w", print_pretty=True):
    """
    Write json to file
    """
    with open(filename, mode) as filey:
        if print_pretty:
            filey.writelines(print_json(json_obj))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def print_json(json_obj):
    """
    Pretty print json.
    """
    return json.dumps(json_obj, indent=4, separators=(",", ": "))


def read_file(filename, mode="r", readlines=True):
    """
    Read content from file.
    """
    with open(filename, mode) as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode="r"):
    """
    Read json from file.
    """
    with open(filename, mode) as filey:
        data = json.load(filey)
    return data


def recursive_find(base, pattern=None):
    """
    Recursively find files below a base.
    """
    if pattern is None:
        pattern = "*"

    for root, dirnames, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)
