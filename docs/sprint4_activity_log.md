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

---

## March 23 – Daily Standup (Monday)

---

## Team Activities
| Who              | Activity |
|------------------|----------|
| Filippa          | Started working on #48 |
| Lisa             | Assisted Filippa with implementation of #48 |
| Team             | Discussed approach for recipe matching and search history |
| Julius & Rickard | Debugged cache pipeline |
| Anton            | Set up frontend |
| Julius           | Set up Supabase |
| Filippa & Lisa   | Implemented statistics using Matplotlib and created new table |
| Team             | Verified that cache-first pipeline is working |
| Team             | Confirmed frontend is running |
| Team             | Confirmed statistics functionality and database table are working |

---