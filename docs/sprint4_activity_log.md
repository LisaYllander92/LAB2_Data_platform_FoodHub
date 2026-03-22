# Sprint 4 – Activity Log
**March 22–27, 2026**

---

## March 22 – Sprint 4 Kickoff (Sunday)

---

## Bug Fixes & Development
| Who     | Activity |
|---------|----------|
| Julius  | Implemented caching with fuzzy search support for curated table |
| Julius  | Pushed branch for team review |
| Rickard | Fixed 4 bugs in cache pipeline (ingredients lookup, json.loads, model_dump, cooking_minutes) and updated docs |


---

## Decisions Made
| Decision | Details |
|----------|---------|
| Search statistics | Save to database first, then read via endpoint |
| Frontend | Plain HTML file calling existing FastAPI routes — no extra setup needed |
| Matplotlib | Proposed for ingredient statistics endpoint |

---

## Current Status
* Cache-first pipeline fully functional and verified.
* **In Progress:** #48 (Search Statistics), frontend HTML, ingredient statistics endpoint.