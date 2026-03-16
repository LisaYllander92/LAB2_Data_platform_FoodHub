import math
from app.schema.internal.recipe_schema import Recipe, Ingredient
from app.schema.spoonacular.recipe_information_schema import SpoonacularRecipeInformation

def clean_numeric(v, default=None):
    if v is None:
        return default
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return default
    return v

def transform_recipe(values: SpoonacularRecipeInformation) -> Recipe:

    ingredients = []
    raw = []
    normalized = []

    for ing in values.extendedIngredients:
        ingredient = Ingredient(
            id=ing.id,
            name=ing.name,
            original=ing.original,
            amount=clean_numeric(ing.amount, 0.0),  # ← ändrad
            unit=ing.unit
        )
        ingredients.append(ingredient)
        raw.append(ing.original)
        normalized.append(ing.name.lower())

    return Recipe(
        id=values.id,
        title=values.title,
        image=values.image,
        servings=clean_numeric(values.servings, 0),                    # ← ändrad
        ready_in_minutes=clean_numeric(values.readyInMinutes, 0),      # ← ändrad
        cooking_minutes=clean_numeric(values.cookingMinutes, 0),       # ← ändrad
        preparation_minutes=clean_numeric(values.preparationMinutes, 0), # ← ändrad
        instructions=values.instructions or "",
        ingredients=ingredients,
        ingredients_raw=raw,
        ingredients_normalized=normalized,
        dish_types=values.dishTypes,
        summary=values.summary or "",
        source_url=values.sourceUrl or ""
    )
# normalized är särskilt viktig — det är den som gör att has_ingredient("avocado") kan matcha mot recepten från Spoonacular.