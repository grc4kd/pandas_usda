import pandas as pd

from usda_load import cleanup_usda_data, decompress_usda_data

json_filename="FoodData_Central_foundation_food_json_2021-10-28.json"

json = decompress_usda_data(
    zip_filename="FoodData_Central_foundation_food_json_2021-10-28.zip", 
    json_filename=json_filename
    )

# read original JSON file in
food_df = pd.read_json(json_filename, orient='records')

# write out records to a new JSON file
im1_filename = "FoodData_IM1.json"
food_sub_json = food_df.to_json(im1_filename)

food_df = pd.read_json(im1_filename, orient='index')

print(food_df.head())