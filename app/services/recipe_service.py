import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # points to Root


def contains_search(ingredients, search):
    if not isinstance(ingredients, list):
        return False
    for item in ingredients:
        if search.lower() in item.lower():
            return True
    return False


def has_ingredient(search: str) -> pd.DataFrame:
    df = pd.read_json(BASE_DIR / "data" / "cleaning_recipe.json")
    match = df["ingredients"].apply(contains_search, search=search)
    matches = df[match]

    output_path = BASE_DIR / "data" / "filtered" / "search_recipe.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    matches.to_json(output_path, orient="records", indent=2)

    return matches