"""Data cleaning pipeline for raw recipe JSON files.

Loads raw recipe data using pandas, standardizes text fields, handles missing 
numeric values, and exports a cleaned JSON file ready for database ingestion.
"""
import json
import pandas as pd


def capitalize_sentences(text: str) -> str:
    """Capitalize the first letter of each sentence in a text block.

    Args:
        text (str): The raw instruction text.

    Returns:
        str: The correctly capitalized text.
    """
    if not isinstance(text, str):
        return text

    sentences = text.split(". ")
    sentences = [s.capitalize() for s in sentences]
    return ". ".join(sentences)


def process_recipe_data(input_path: str = "recipes_raw.json", output_path: str = "cleaning_recipe.json"):
    """Load, clean, and export the recipe dataset.

    Args:
        input_path (str): File path to the raw JSON data.
        output_path (str): File path for the cleaned JSON output.
    """
    with open(input_path) as f:
        data = json.load(f).copy()

    recipes_df = pd.DataFrame(data)

    print("=== RAW DATA ===")
    print(recipes_df)
    print("\nDtypes:")
    print(recipes_df.dtypes)

    # Title
    recipes_df["title"] = recipes_df["title"].str.replace(r"\s+", " ", regex=True).str.strip().str.title()

    # Cooking time
    recipes_df["cooking_minutes"] = pd.to_numeric(recipes_df["cooking_minutes"], errors="coerce").fillna(0).astype(int)

    # Servings
    recipes_df["servings"] = pd.to_numeric(recipes_df["servings"], errors="coerce").fillna(0).astype(int)

    # Image
    recipes_df["image"] = recipes_df["image"].replace("", None)

    # Ingredients
    cleaned_ingredients = []
    for items in recipes_df["ingredients"]:
        if isinstance(items, list):
            cleaned_ingredients.append([i.strip().lower() for i in items])
        else:
            cleaned_ingredients.append(items)

    recipes_df["ingredients"] = cleaned_ingredients

    # Instructions
    recipes_df["instructions"] = recipes_df["instructions"].str.replace(r"\.\s*", ". ", regex=True)
    recipes_df["instructions"] = recipes_df["instructions"].apply(capitalize_sentences).str.strip()

    # Allergies
    recipes_df["allergies"] = recipes_df["allergies"].apply(
        lambda x: list(set(i.lower().strip() for i in x)) if isinstance(x, list) else x
    )

    recipes_df.to_json(output_path, orient="records", indent=2)
    print(f"\nCleaned data saved to {output_path}")


if __name__ == "__main__":
    process_recipe_data()