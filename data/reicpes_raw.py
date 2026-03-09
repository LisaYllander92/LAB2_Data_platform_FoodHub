import json 
import pandas as pd

with open("recipes_raw.json") as f: 
    data = json.load(f)

recipes_df = pd.DataFrame(data)
print("=== RAW DATA ===")
print(recipes_df)
print("\nDtypes:")
print(recipes_df.dtypes)

####### Title #######
recipes_df["title"] = recipes_df["title"].str.upper()

###### Cooking time #######
recipes_df["cooking_minutes"] = pd.to_numeric(recipes_df["cooking_minutes"], errors="coerce")
recipes_df["cooking_minutes"] = recipes_df["cooking_minutes"].fillna(0).astype(int) # visst skulle det vara int? 

####### Servings ########
recipes_df["servings"] = pd.to_numeric(recipes_df["servings"], errors="coerce")
recipes_df["servings"] = recipes_df["servings"].fillna(0).astype(int)

####### image #######
print(recipes_df["image"])
recipes_df["image"] = recipes_df["image"].replace("", None)

print(recipes_df["image"])
