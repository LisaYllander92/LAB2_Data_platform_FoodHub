import matplotlib.pyplot as plt
import io
#import seaborn as sns
from app.repositories import recipe_repository

def plot_popular_searches() -> bytes:
    """Generate a bar chart of the most popular searches and return as PNG bytes."""
    data = recipe_repository.get_popular_searches()

    if not data:
        return None

    queries = [d["query"] for d in data]
    counts = [d["count"] for d in data]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(queries, counts, color="#1D9E75")  # ← barh → bar
    ax.set_ylabel("Number of searches")       # ← xlabel → ylabel
    ax.set_xlabel("Ingredients")              # ← lägg till
    ax.set_title("Most popular searches")
    plt.xticks(rotation=45, ha="right")       # ← snedställ etiketterna
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf.read()