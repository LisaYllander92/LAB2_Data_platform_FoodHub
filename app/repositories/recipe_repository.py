import json
from app.database import pool

def get_cached_by_terms(search_terms: list[str], limit: int):
    conditions = " AND ".join(
        ["ingredients_normalized::text ILIKE %s"] * len(search_terms)
    )
    params = [f"%{term.lower()}%" for term in search_terms] + [limit]
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT title, image, cooking_minutes, servings, instructions,
                       ingredients, ingredients_normalized
                FROM curated_recipes
                WHERE {conditions}
                AND ingredients_normalized IS NOT NULL
                LIMIT %s
            """, params)
            return cur.fetchall()

def get_all_cached():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, image, cooking_minutes, servings, instructions,
                       ingredients, ingredients_normalized
                FROM curated_recipes
                WHERE ingredients_normalized IS NOT NULL
            """)
            return cur.fetchall()

def save_recipe(recipe: dict):
    with pool.connection() as conn:
        conn.execute("""
            INSERT INTO curated_recipes
                (title, image, cooking_minutes, servings, instructions,
                 ingredients, ingredients_normalized)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (title) DO NOTHING
        """, (
            recipe.get("title"),
            recipe.get("image"),
            recipe.get("cooking_minutes") or recipe.get("ready_in_minutes") or 0,
            recipe.get("servings"),
            recipe.get("instructions"),
            json.dumps(recipe.get("ingredients_raw", [])),
            json.dumps(recipe.get("ingredients_normalized", []))
        ))

def get_history(limit: int):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, image, cooking_minutes, servings, created_at
                FROM curated_recipes
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

def get_by_title(title: str):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, image, cooking_minutes, servings, instructions,
                       ingredients, ingredients_normalized
                FROM curated_recipes
                WHERE LOWER(title) = LOWER(%s)
            """, (title,))
            return cur.fetchone()


#@router.get("/recipes/popular-searches")
def get_popular_searches():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT query, COUNT(*) AS search_count
                FROM search_log
                GROUP BY query
                ORDER BY search_count DESC, query ASC
                LIMIT 10
            """)
            rows = cur.fetchall()
    return [{"query": row[0], "count": row[1]} for row in rows]