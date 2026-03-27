"""Data validation script to flag unreasonable or invalid recipe data.

Reads a cleaned recipe dataset and identifies rows with impossible 
cooking times or serving sizes, exporting these flagged records 
to a separate file for review.
"""
import pandas as pd


def get_flag_reason(row: pd.Series) -> list:
    """Determine the specific reasons a recipe row was flagged.

    Checks the cooking_minutes and servings columns against predefined 
    acceptable ranges and generates descriptive error messages.

    Args:
        row (pd.Series): A single row from the recipe DataFrame.

    Returns:
        list: A list of string messages detailing why the row was flagged, 
            or None if no issues are found.
    """
    reasons = []

    if pd.isna(row["cooking_minutes"]):
        reasons.append(f"Invalid cooking time: '{row['cooking_minutes']}'")
    elif row["cooking_minutes"] <= 0 or row["cooking_minutes"] > 600:
        reasons.append(f"Unreasonable cooking time: {row['cooking_minutes']} min")

    if pd.notna(row["servings"]) and (row["servings"] <= 0 or row["servings"] > 100):
        reasons.append(f"Unreasonable number of servings: {row['servings']}")

    return reasons if reasons else None


def flag_invalid_recipes(input_path: str = "cleaning_recipe.json", output_path: str = "flagged_values.json"):
    """Filter and export recipes that contain data anomalies.

    Applies boundary conditions to cooking times and servings, extracts
    the rows failing these checks, appends the specific flag reasons,
    and exports the result to a JSON file.

    Args:
        input_path (str): File path to the cleaned JSON data.
        output_path (str): File path for the flagged JSON output.
    """
    df = pd.read_json(input_path)
    flagged_df = df.copy()

    wrong_minutes_condition = (
        (flagged_df["cooking_minutes"] <= 0) |
        (flagged_df["cooking_minutes"] > 600)
    )

    wrong_serving_condition = (
        (flagged_df["servings"] <= 0) |
        (flagged_df["servings"] > 100)
    )

    flagged_df["is_flagged"] = wrong_minutes_condition | wrong_serving_condition

    # Use .copy() to avoid pandas SettingWithCopyWarning
    flagged_dataframe = flagged_df[flagged_df["is_flagged"]].copy()

    if not flagged_dataframe.empty:
        flagged_dataframe["flag_reasons"] = flagged_dataframe.apply(get_flag_reason, axis=1)
        flagged_dataframe.to_json(output_path, orient="records", indent=2)
        print(f"Flagged {len(flagged_dataframe)} recipes and saved to {output_path}")
    else:
        print("No recipes were flagged.")


if __name__ == "__main__":
    flag_invalid_recipes()