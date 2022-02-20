import pandas as pd

from usda_load import cleanup_usda_data, decompress_usda_data

json = decompress_usda_data(
    zip_filename="FoodData_Central_foundation_food_json_2021-10-28.zip", 
    json_filename="FoodData_Central_foundation_food_json_2021-10-28.json"
    )

food_df = pd.DataFrame(json)

print(food_df.head())