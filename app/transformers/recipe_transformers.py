"""Transformer functions to convert external API responses into internal schemas.

Handles the mapping of Spoonacular data models to the internal Recipe
models, ensuring data consistency, handling missing numeric values, 
and normalizing ingredients for accurate search filtering.
"""
import math
from app.schema.internal.recipe_schema import Recipe, Ingredient
from app.schema.spoonacular.recipe_information_schema import SpoonacularRecipeInformation


def clean_numeric(v, default=None):
    """Clean numeric values by replacing None, NaN, or Inf with a default value.

    Args:
        v (Any): The numeric value to clean.
        default (Any, optional): The fallback value if v is invalid. Defaults to None.

    Returns:
        Any: The cleaned numeric value or the fallback default.
    """
    if v is None:
        return default
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return default
    return v


def transform_recipe(values: SpoonacularRecipeInformation) -> Recipe:
    """Transform a Spoonacular recipe response into the internal Recipe schema.

    Extracts ingredients, applies numeric cleaning, and normalizes data. 
    The normalization of ingredient names is particularly important, as it 
    enables the `has_ingredient` function to properly match search queries 
    against the external Spoonacular recipes.

    Args:
        values (SpoonacularRecipeInformation): The raw recipe data from Spoonacular.

    Returns:
        Recipe: The transformed internal recipe object.
    """
    ingredients = []
    raw = []
    normalized = []

    for ing in values.extendedIngredients:
        ingredient = Ingredient(
            id=ing.id,
            name=ing.name,
            original=ing.original,
            amount=clean_numeric(ing.amount, 0.0),
            unit=ing.unit
        )
        ingredients.append(ingredient)
        raw.append(ing.original)
        normalized.append(ing.name.lower())

    return Recipe(
        id=values.id,
        title=values.title,
        image=values.image,
        servings=clean_numeric(values.servings, 0),
        ready_in_minutes=clean_numeric(values.readyInMinutes, 0),
        cooking_minutes=clean_numeric(values.cookingMinutes, 0),
        preparation_minutes=clean_numeric(values.preparationMinutes, 0),
        instructions=values.instructions or "",
        ingredients=ingredients,
        ingredients_raw=raw,
        ingredients_normalized=normalized,
        dish_types=values.dishTypes,
        summary=values.summary or "",
        source_url=values.sourceUrl or ""
    )