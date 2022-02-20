import os, shutil, errno
import unittest


from usda_load import decompress_usda_data, cleanup_usda_data

# DRY file not found error
def FNF_ERR(filename):
    raise FileNotFoundError(
        errno.ENOENT,
        os.strerror(errno.ENOENT),
        filename
    )

# try to load testfile over filename
# if the file is not already loaded
# TODO check file contents before each test
def try_loadtestfile(testfile, filename):
    if not os.path.exists(filename):
        if not os.path.exists(testfile):
            FNF_ERR(testfile)
        shutil.copy(testfile, filename)

# start test class
class TestUSDALoadMethods(unittest.TestCase):
    # run setUp(self) between each unit test
    # make sure both ZIP and JSON data files are loaded
    def setUp(self):
        # re-import test data as needed between each test
        zip_testfile = "testfiles/FoodData_Central_foundation_food_json_2021-10-28.zip"
        zip_filename = "FoodData_Central_foundation_food_json_2021-10-28.zip"
        json_testfile = "testfiles/FoodData_Central_foundation_food_json_2021-10-28.json"
        json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"

        try_loadtestfile(zip_testfile, zip_filename)
        try_loadtestfile(json_testfile, json_filename)


    def test_decompress_usda_data(self):
        zip_filename = "FoodData_Central_foundation_food_json_2021-10-28.zip"
        json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"

        decompress_usda_data(zip_filename, json_filename)

        self.assertTrue(os.path.exists(json_filename))


    def test_cleanup_usda_data(self):
        json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"
        
        self.assertTrue(os.path.exists(json_filename))
        
        cleanup_usda_data(json_filename)

        self.assertFalse(os.path.exists(json_filename))


if __name__ == '__main__':
    unittest.main()