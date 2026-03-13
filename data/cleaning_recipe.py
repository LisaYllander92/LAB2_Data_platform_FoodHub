import json 
import pandas as pd

with open("recipes_raw.json") as f: 
    data = json.load(f).copy()

recipes_df = pd.DataFrame(data)
print("=== RAW DATA ===")
print(recipes_df)
print("\nDtypes:")
print(recipes_df.dtypes)

####### Title #######
recipes_df["title"] = recipes_df["title"].str.replace(r"\s+", " ", regex=True).str.strip().str.title()

###### Cooking time #######
recipes_df["cooking_minutes"] = pd.to_numeric(recipes_df["cooking_minutes"], errors="coerce")
recipes_df["cooking_minutes"] = recipes_df["cooking_minutes"].fillna(0).astype(int) # Todo: filter later - "missing value"

####### Servings ########
recipes_df["servings"] = pd.to_numeric(recipes_df["servings"], errors="coerce")
recipes_df["servings"] = recipes_df["servings"].fillna(0).astype(int) # Todo: filter later - "missing value"

####### image #######
print(recipes_df["image"])
recipes_df["image"] = recipes_df["image"].replace("", None)
print(recipes_df["image"])

####### Ingredients #######
print(recipes_df["ingredients"])
recipes_df["ingredients"] = {
    index: [i.strip() for i in ingredients]
    for index, ingredients in recipes_df["ingredients"].items()
    if isinstance(ingredients, list)
        }

cleaned = []

for items in recipes_df["ingredients"]:       # loop over each cell
    if isinstance(items, list):
        stripped = []
        for i in items:                        # loop over each ingredient
            stripped.append(i.strip().lower())
        cleaned.append(stripped)
    else:
        cleaned.append(items)                  # not a list, keep as-is
recipes_df["ingredients"] = cleaned

print(recipes_df["ingredients"]) # Todo: check charset for whitespace after number


####### Instructions ########
def capitalize_sentences(text):
    sentences = text.split(". ")
    sentences = [s.capitalize() for s in sentences]
    return ". ".join(sentences)
recipes_df["instructions"] = recipes_df["instructions"].str.replace(r"\.\s*", ". ", regex=True)
recipes_df["instructions"] = recipes_df["instructions"].apply(capitalize_sentences).str.strip()

####### Allergies #######
recipes_df["allergies"] = recipes_df["allergies"].apply(lambda x: list(set(i.lower().strip() for i in x))if isinstance(x, list) else x)


recipes_df.to_json("cleaning_recipe.json", orient= "records", indent=2)
