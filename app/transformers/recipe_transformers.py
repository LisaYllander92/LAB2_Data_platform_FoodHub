from app.schema.internal.recipe_schema import Recipe, Ingredient
from app.schema.spoonacular.recipe_information_schema import (
    SpoonacularRecipeInformation
)


def transform_recipe(values: SpoonacularRecipeInformation) -> Recipe:

    ingredients = []
    raw = []
    normalized = []

    for ing in values.extendedIngredients:

        ingredient = Ingredient(
            id=ing.id,
            name=ing.name,
            original=ing.original,
            amount=ing.amount,
            unit=ing.unit
        )
        ingredients.append(ingredient)
        raw.append(ing.original)
        normalized.append(ing.name.lower())

    return Recipe(
        id=values.id,
        title=values.title,
        image=values.image,
        servings=values.servings,
        ready_in_minutes=values.readyInMinutes,
        cooking_minutes=values.cookingMinutes,
        preparation_minutes=values.preparationMinutes,
        instructions=values.instructions,
        ingredients=ingredients,
        ingredients_raw=raw,
        ingredients_normalized=normalized,
        dish_types=values.dishTypes,
        summary=values.summary,
        source_url=values.sourceUrl
    )