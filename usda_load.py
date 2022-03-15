import json
import zipfile
import os
import errno
import pandas as pd

# set up logging
import logging
import logging.config
# create console handler and set level to debug
if not os.path.exists("logs"):
    os.mkdir("logs")
logging.config.fileConfig("logging.conf")
logger = logging.getLogger("basicLogger")
fh = logging.FileHandler("logs/logging.txt")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

def FNF_ERR(filename):
    # DRY file not found error
    raise FileNotFoundError(
        errno.ENOENT,
        os.strerror(errno.ENOENT),
        filename
    )


def decompress_usda_data(zip_filename, json_filename):
    if not os.path.exists(zip_filename):
        logger.info(f"Can't find zip file {zip_filename}")
        FNF_ERR(zip_filename)
    if not os.path.exists(json_filename):
        logger.info(f"Unzipping json file {json_filename}")
        with zipfile.ZipFile(zip_filename) as zf:
            zf.extract(json_filename)
    else:
        logger.info("JSON data exists, skipping unzip operation")

    # load JSON from file return Python object to caller
    with open(json_filename) as f:
        data = json.load(f)
        return data


def cleanup_usda_data(json_filename):
    if os.path.exists(json_filename):
        logger.info(f"Removing JSON file {json_filename}")
        os.remove(json_filename)


def load_all_foods(json_filename):
    df_foods = pd.read_json(json_filename)

    all_foods = {}

    # parse the JSON in USDA format FoundationFoods is root element
    for food in df_foods["FoundationFoods"]:
        # each food has a list of inputFoods that are parented by FoundationFoods
        for inputFoods in food["inputFoods"]:
            # append all results to a flat dictionary of input foods
            all_foods[inputFoods["id"]] = inputFoods

    return all_foods
