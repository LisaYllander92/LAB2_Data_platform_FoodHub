import pandas as pd
from pathlib import Path
from rapidfuzz import fuzz

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # points to Root

THRESHOLD = 80

def contains_search(ingredients, search):
    if not isinstance(ingredients, list):
        return False
    for item in ingredients:
        if search.lower() in item.lower():
            return True
        if fuzz.partial_ratio(search.lower(), item.lower()) >= THRESHOLD: #fuzzy match,returns true if score meets THRESHOLD
            return True #
    return False


def has_ingredient(search: str) -> pd.DataFrame:
    df = pd.read_json(BASE_DIR / "data" / "cleaning_recipe.json")
    search_terms = [s.strip() for s in search.replace(",", " ").split()] # splits search string into individual terms

    mask = pd.Series([True] * len(df), index=df.index) #

    for term in search_terms: #
        match = df["ingredients"].apply(contains_search, search=term) # 
        mask = mask & match
        
    matches = df[mask]
    
    output_path = BASE_DIR / "data" / "filtered" / "search_recipe.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    matches.to_json(output_path, orient="records", indent=2)

    return matches