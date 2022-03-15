import json
import os
import shutil
import unittest
import zipfile
import usda_load


def _decompress_usda_data(zip_filename, json_filename):
    if not os.path.exists(zip_filename):
        print(f"Can't find zip file {zip_filename}")
        usda_load.FNF_ERR(zip_filename)
    if not os.path.exists(json_filename):
        print(f"Unzipping json file {json_filename}")
        with zipfile.ZipFile(zip_filename) as zf:
            zf.extract(json_filename)
    else:
        print("JSON data exists, skipping unzip operation")

    # load JSON from file
    # return Python object to caller
    with open(json_filename) as f:
        data = json.load(f)
        return data


# start test class
class TestUSDALoadMethods(unittest.TestCase):
    # run setUp(self) between each unit test
    # make sure both ZIP and JSON data files are loaded
    # into the live folder. This is the expected state
    # before running any test in this class
    def setUp(self):
        # re-import test data as needed between each test
        zip_testfile = "testfiles/FoodData_Central_foundation_food_json_2021-10-28.zip"
        zip_filename = "FoodData_Central_foundation_food_json_2021-10-28.zip"
        json_testfile = "testfiles/FoodData_Central_foundation_food_json_2021-10-28.json"
        json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"

        # files in the testfiles directory are backing files and should be handled first
        if not os.path.exists(zip_testfile):
            # a zip file is required at ./testfiles/FoodData_Central_foundation_food_json_2021-10-28.zip
            raise usda_load.FNF_ERR(
                f"cannot continue, a required zip file is missing at {zip_testfile}")
        # extract the zip file into the backing directory, trading space for convenience
        if not os.path.exists(json_testfile):
            with zipfile.ZipFile(zip_filename) as zf:
                zf.extract(json_filename)
        # copy backing file over missing live file
        if not os.path.exists(zip_filename):
            shutil.copy(zip_testfile, zip_filename)
        if not os.path.exists(json_filename):
            shutil.copy(json_testfile, json_filename)

    def test_decompress_usda_data(self):
        zip_filename = "FoodData_Central_foundation_food_json_2021-10-28.zip"
        json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"

        # clear file before decompression test
        os.remove(json_filename)

        usda_load.decompress_usda_data(zip_filename, json_filename)

        self.assertTrue(os.path.exists(json_filename))

    def test_cleanup_usda_data(self):
        json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"

        self.assertTrue(os.path.exists(json_filename))

        usda_load.cleanup_usda_data(json_filename)

        self.assertFalse(os.path.exists(json_filename))

    def test_decompress_usda_data_FNF_ERR(self):
        # file should not exist
        zip_filename = "ThatoneFileI_was_lookingfor.zip"
        json_filename = "FoodData.json"

        with self.assertRaises(FileNotFoundError):
            usda_load.decompress_usda_data(zip_filename, json_filename)

    def test_get_usda_data(self):
        json = usda_load.decompress_usda_data(
            zip_filename="FoodData_Central_foundation_food_json_2021-10-28.zip",
            json_filename="FoodData_Central_foundation_food_json_2021-10-28.json"
        )

        self.assertGreater(len(json), 0)

    def test_load_all_foods(self):
        json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"
        json_data = usda_load.decompress_usda_data(
            zip_filename="FoodData_Central_foundation_food_json_2021-10-28.zip",
            json_filename=json_filename
        )

        # load a dictionary of all foods
        flat_foods = usda_load.load_all_foods(json_filename)

        # there should be more than 200 foods
        self.assertGreater(len(flat_foods), 200)

        # test one dictionary lookup
        self.assertEqual(
            flat_foods.get(10922),
            {
                "id": 10922,
                "foodDescription": "Mustard, yellow, FRENCHS CLASSIC (CO,CT) - CY120PW",
                "inputFood": {
                    "foodClass": "Composite",
                    "description": "Mustard, yellow, FRENCHS CLASSIC (CO,CT) - CY120PW",
                    "foodCategory": {
                        "id": 2, "code": "0200", "description": "Spices and Herbs"
                    },
                    "fdcId": 326494,
                    "dataType": "Sample",
                    "publicationDate": "4/1/2019"
                }
            }
        )


if __name__ == '__main__':
    unittest.main()
