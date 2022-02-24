import pandas as pd

from usda_load import cleanup_usda_data, decompress_usda_data

json_filename="FoodData_Central_foundation_food_json_2021-10-28.json"

json = decompress_usda_data(
    zip_filename="FoodData_Central_foundation_food_json_2021-10-28.zip", 
    json_filename=json_filename
    )

# read original JSON file in
df_foods = pd.read_json(json_filename)
df_foods = pd.json_normalize(df_foods.FoundationFoods)

# create subset of foods pandas object
# where the food has a scientific name data
df_sci_foods = df_foods[df_foods["scientificName"].notna()]

print(df_sci_foods.head())