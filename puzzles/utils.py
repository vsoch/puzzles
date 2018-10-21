'''

Copyright (c) 2018 Vanessa Sochat

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

import fnmatch
import json
import os
import re
import requests
import tempfile
from puzzles.logger import bot
from collections import OrderedDict
import sys

# Python less than version 3 must import OSError
if sys.version_info[0] < 3:
    from exceptions import OSError


################################################################################
# Local commands and requests
################################################################################

def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(__file__))


def get_temporary_name(prefix=None, ext=None):
    '''get a temporary name, can be used for a directory or file. This does so
       without creating the file, and adds an optional prefix
  
       Parameters
       ==========
       prefix: if defined, add the prefix after deid
       ext: if defined, return the file extension appended. Do not specify "."
    '''
    default_prefix = 'puzzles-'
    if prefix:
        default_prefix = 'puzzles-%s-' % prefix

    tmpname = os.path.join(tempfile.gettempdir(), 
                           '%s%s' % (default_prefix,
                                     next(tempfile._get_candidate_names())))
    if ext:
        tmpname = '%s.%s' % (tmpname, ext)
    return tmpname


################################################################################
## FILE OPERATIONS #############################################################
################################################################################

def copyfile(source, destination, force=True):
    '''copy a file from a source to its destination.
    '''
    # Case 1: It's already there, we aren't replacing it :)
    if source == destination and force is False:
        return destination

    # Case 2: It's already there, we ARE replacing it :)
    if os.path.exists(destination) and force is True:
        os.remove(destination)

    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode="w"):
    '''write_file will open a file, "filename" and write content, "content"
       and properly close the file
    '''
    with open(filename, mode) as filey:
        filey.writelines(content)
    return filename


def write_json(json_obj, filename, mode="w", print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file

       Parameters
       ==========
       json_obj: the dict to print to json
       filename: the output file to write to
       pretty_print: if True, will use nicer formatting
    '''
    with open(filename, mode) as filey:
        if print_pretty:
            filey.writelines(print_json(json_obj))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename


def print_json(json_obj):
    ''' just dump the json in a "pretty print" format
    '''
    return json.dumps(
                    json_obj,
                    indent=4,
                    separators=(
                        ',',
                        ': '))


def read_file(filename, mode="r", readlines=True):
    '''write_file will open a file, "filename" and write content, "content"
       and properly close the file
    '''
    with open(filename, mode) as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_json(filename, mode='r'):
    '''read_json reads in a json file and returns
       the data structure as dict.
    '''
    with open(filename, mode) as filey:
        data = json.load(filey)
    return data


def recursive_find(base, pattern=None):
    '''recursive find will yield dicom files in all directory levels
       below a base path. It uses get_dcm_files to find the files in the bases.
    '''
    if pattern is None:
        pattern = "*"

    for root, dirnames, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)
