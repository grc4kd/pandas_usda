import os

from usda_load import decompress_usda_data, cleanup_usda_data


def test_decompress_usda_data():
    zip_filename = "FoodData_Central_foundation_food_json_2021-10-28.zip"
    json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"

    decompress_usda_data(zip_filename, json_filename)

    assert os.path.exists(json_filename)


def test_cleanup_usda_data():
    json_filename = "FoodData_Central_foundation_food_json_2021-10-28.json"

    assert os.path.exists(json_filename)
    
    cleanup_usda_data()

    assert (not os.path.exists(json_filename))