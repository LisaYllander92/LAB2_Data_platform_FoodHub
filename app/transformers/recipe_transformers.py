"""Transformer functions to convert Spoonacular API responses into internal schemas."""
import math
from app.schema.internal.recipe_schema import Recipe, Ingredient
from app.schema.spoonacular.recipe_information_schema import SpoonacularRecipeInformation


def clean_numeric(v, default=None):
    """Replace None, NaN, or Inf with a default value for safe numeric handling."""
    if v is None:
        return default
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return default
    return v


def transform_recipe(values: SpoonacularRecipeInformation) -> Recipe:
    """Transform a Spoonacular recipe response into the internal Recipe schema.

    Normalizes ingredient names to lowercase, which enables has_ingredient()
    to match search queries against Spoonacular recipes via fuzzy search.
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