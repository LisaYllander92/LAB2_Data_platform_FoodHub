import pandas as pd
from pathlib import Path
from rapidfuzz import fuzz

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # points to Root

THRESHOLD = 80

def contains_search(ingredients, search):
    if not isinstance(ingredients, list):
        return False
    for item in ingredients:
        if isinstance(item, dict):
            searchable = item.get("name", " ".join(str(v) for v in item.values()))
        elif isinstance(item, str):
            searchable = item
        else:
            continue

        if search.lower() in searchable.lower():
            return True
        if fuzz.partial_ratio(search.lower(), searchable.lower()) >= THRESHOLD:
            return True

    return False


def has_ingredient(search: str, df: pd.DataFrame = None, save: bool = True) -> pd.DataFrame:
    loaded_from_disk = df is None

    if loaded_from_disk:
        df = pd.read_json(BASE_DIR / "data" / "cleaning_recipe.json")

    #print(df["ingredients"].iloc[0])
    search_terms = [s.strip() for s in search.replace(",", " ").split()]
    mask = pd.Series([True] * len(df), index=df.index)
    for term in search_terms:
        match = df["ingredients"].apply(contains_search, search=term)
        mask = mask & match

    matches = df[mask]

    if save and loaded_from_disk:
        output_path = BASE_DIR / "data" / "filtered" / "search_recipe.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        matches.to_json(output_path, orient="records", indent=2)

    return matches