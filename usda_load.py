import json
from re import L
import zipfile
import os, errno

# DRY file not found error
def FNF_ERR(filename):
    raise FileNotFoundError(
        errno.ENOENT,
        os.strerror(errno.ENOENT),
        filename
    )


def decompress_usda_data(zip_filename, json_filename):
    if not os.path.exists(zip_filename):
        print (f"Can't find zip file {zip_filename}")
        FNF_ERR(zip_filename)
    if not os.path.exists(json_filename):
        print (f"Unzipping json file {json_filename}")
        with zipfile.ZipFile(zip_filename) as zf:
            zf.extract(json_filename)
    else:
        print ("JSON data exists, skipping unzip operation")
    
    # load JSON from file
    # return Python object to caller
    with open(json_filename) as f:
        data = json.load(f)
        return data


def cleanup_usda_data(json_filename):
    if os.path.exists(json_filename):
        print (f"Removing JSON file {json_filename}")
        os.remove(json_filename)
