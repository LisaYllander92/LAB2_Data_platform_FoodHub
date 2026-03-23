"""Service for searching and filtering recipes by ingredients.

Uses exact matching and fuzzy string matching (RapidFuzz) to find
recipes containing specific ingredients from a pandas DataFrame.
"""
import pandas as pd
from pathlib import Path
from rapidfuzz import fuzz

BASE_DIR = Path(__file__).resolve().parent.parent.parent
THRESHOLD = 80


def contains_search(ingredients, search):
    """Check if a search term matches any item in an ingredient list.

    Supports both exact substring matching and fuzzy matching to account
    for slight misspellings or variations in ingredient names.

    Args:
        ingredients (list): A list of ingredients (strings or dictionaries).
        search (str): The specific ingredient term to search for.

    Returns:
        bool: True if a match or partial match is found, otherwise False.
    """
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
    """Filter a DataFrame of recipes based on a string of ingredients.

    Splits the search string into individual terms and filters the data
    so only recipes containing all the specified terms are returned. Loads
    data from a local JSON file if no DataFrame is provided.

    Args:
        search (str): Comma or space-separated ingredient terms to search for.
        df (pd.DataFrame, optional): Existing recipe DataFrame. Defaults to None.
        save (bool, optional): Save the filtered results to disk. Defaults to True.

    Returns:
        pd.DataFrame: A DataFrame containing only the matching recipes.
    """
    loaded_from_disk = df is None

    if loaded_from_disk:
        df = pd.read_json(BASE_DIR / "data" / "cleaning_recipe.json")

    search_terms = [s.strip() for s in search.replace(",", " ").split()]
    #mask = pd.Series([True] * len(df), index=df.index)

    # for term in search_terms:
    #     match = df["ingredients"].apply(contains_search, search=term)
    #     mask = mask & match

    #    matches = df[mask]

    # Count how many terms match per recipe and sort by most matches
    df["match_count"] = sum(
        df["ingredients"].apply(contains_search, search=term).astype(int)
        for term in search_terms
    )

    # Filter out recipes with 0 matches and sort by most matches first
    matches = df[df["match_count"] > 0].sort_values("match_count", ascending=False)
    matches = matches.drop(columns=["match_count"])

    if save and loaded_from_disk:
        output_path = BASE_DIR / "data" / "filtered" / "search_recipe.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        matches.to_json(output_path, orient="records", indent=2)

    return matches