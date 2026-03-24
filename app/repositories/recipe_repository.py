"""Database access functions for retrieving and storing recipes and search statistics."""
import json
from app.database import pool


def get_cached_by_terms(search_terms: list[str], limit: int):
    """Query curated_recipes for rows where ingredients_normalized matches any search term."""
    conditions = " OR ".join(
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
    """Return all rows from curated_recipes that have normalized ingredients."""
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
    """Insert a recipe into curated_recipes, skipping duplicates by title."""
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
    """Return the most recently added recipes from curated_recipes."""
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
    """Return a single recipe from curated_recipes matching the given title (case-insensitive)."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, image, cooking_minutes, servings, instructions,
                       ingredients, ingredients_normalized
                FROM curated_recipes
                WHERE LOWER(title) = LOWER(%s)
            """, (title,))
            return cur.fetchone()


def get_popular_searches():
    """Return the top 10 most frequently searched queries from search_log."""
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


def mark_viewed(title: str):
    """Update last_viewed_at timestamp for a recipe when it is opened by a user."""
    with pool.connection() as conn:
        conn.execute("""
            UPDATE curated_recipes
            SET last_viewed_at = CURRENT_TIMESTAMP
            WHERE LOWER(title) = LOWER(%s)
        """, (title,))


def get_stats():
    """Return aggregated statistics including popular searches, recently viewed recipes, and totals."""
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Popular searches
            cur.execute("""
                SELECT query, COUNT(*) AS search_count
                FROM search_log
                GROUP BY query
                ORDER BY search_count DESC
                LIMIT 10
            """)
            popular = [{"query": row[0], "count": row[1]} for row in cur.fetchall()]

            # Most recently viewed recipes
            cur.execute("""
                SELECT title, cooking_minutes, servings
                FROM curated_recipes
                WHERE last_viewed_at IS NOT NULL
                ORDER BY last_viewed_at DESC
                LIMIT 5
            """)
            recent = [{"title": row[0], "cooking_minutes": row[1], "servings": row[2]} for row in cur.fetchall()]

            # Total counts
            cur.execute("SELECT COUNT(*) FROM curated_recipes")
            total_recipes = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM search_log")
            total_searches = cur.fetchone()[0]

    return {
        "popular": popular,
        "recent": recent,
        "total_recipes": total_recipes,
        "total_searches": total_searches
    }

""" def log_search_query(query: str) -> None:
   # Split the query into individual terms and insert each into search_log.
    terms = [t.strip().lower() for t in query.replace(",", " ").split() if t.strip()]

    if not terms:
        return

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO search_log (query) VALUES (%s)", [(term,) for term in terms])
        conn.commit()"""

def log_search_query(query: str):
    """Loggar söktermer för statistik."""
    terms = [t.strip() for t in query.split(",") if t.strip()]
    if not terms:
        return

    with pool.connection() as conn:
        with conn.cursor() as cur:
            # Vi kör en vanlig loop istället för executemany
            # för att undvika DuplicatePreparedStatement-felet.
            for term in terms:
                cur.execute(
                    "INSERT INTO search_log (query) VALUES (%s)",
                    (term,),
                    prepare = False
                )