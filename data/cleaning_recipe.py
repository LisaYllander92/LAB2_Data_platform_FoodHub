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

recipes_df["title"] = recipes_df["title"].str.replace(r"\s+", " ", regex=True).str.title()


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

####### Ingredients #######
"""print(recipes_df["ingredients"])
recipes_df["ingredients"] = recipes_df["ingredients"].replace("", None)
recipes_df["ingredients"] = recipes_df["ingredients"].str.strip()
recipes_df["ingredients"] = recipes_df["ingredients"].str.title()

print(recipes_df["ingredients"])"""


####### Instructions ########

recipes_df.to_csv("cleaning_recipe.csv", index=False)

