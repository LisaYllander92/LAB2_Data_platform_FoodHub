import json
import pandas as pd
from app.schema.internal.schema import FoodData

df = pd.read_json("cleaning_recipe.json")
flagged_df = df.copy()

def get_flag_reason(row):
    reasons = []

    if pd.isna(row["cooking_minutes"]):
        reasons.append(f"Invalid cooking time: '{row['cooking_minutes']}'")
    if pd.notna(row["cooking_minutes"]) and (row["cooking_minutes"] <= 0 or row["cooking_minutes"] > 600):
        reasons.append(f"Unreasonable cooking time: {row['cooking_minutes']} min")
    if pd.notna(row["servings"]) and (row["servings"] <= 0 or row["servings"] > 100):
        reasons.append(f"Unreasonable number of potions: {row['servings']}")

    return reasons if reasons else None

wrong_minutes_condition = (
    (flagged_df["cooking_minutes"] < 0) |
    (flagged_df["cooking_minutes"] > 600) |
    ((flagged_df["cooking_minutes"] == 0) & flagged_df["cooking_minutes"].notna())
)

wrong_serving_condition = (
    (flagged_df["servings"] < 0) |
    (flagged_df["servings"] > 100) |
    (flagged_df["servings"] == 0)
    & flagged_df["servings"].notna()
)

flagged_df["is_flagged"] = (
    wrong_minutes_condition |
    wrong_serving_condition
)

flagged_dataframe = flagged_df[flagged_df["is_flagged"] == True]

flagged_dataframe["flag_reasons"] = flagged_dataframe.apply(get_flag_reason, axis=1)
flagged_dataframe.to_json("flagged_values.json", orient= "records", indent=2)



