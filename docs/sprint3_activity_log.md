# Sprint 3 – Activity Log
**March 16–19, 2026**

---

## March 12 – Sprint 3 Kickoff (Standup & Planning)
**Attendees:** Rickard, Lisa, Anton, Julius, Filippa

### Planning Poker
| Story | Description | Average Points |
|-------|-------------|---------------|
| #4 | (validation) – average 6.8
| #8 | Spoonacular API | 14.6 |
| #17 | Spell correction | 10.0 |

### Task Distribution
| Who | Task |
|-----|------|
| Rickard | #26 – Kafka producer |
| Lisa | #26 – Kafka topic configuration |
| Anton | #8 – Spoonacular API |
| Julius | #17 – Rapidfuzz integration |
| Filippa | Data modeling completion *(ongoing)* |

### Delivered
| Who | Delivery |
|-----|----------|
| Lisa | Implemented topic configuration in Kafka |
| Rickard | Built Kafka producer logic, created `init.sql` table |
| Julius | Integrated rapidfuzz for ingredient matching |
| Anton | Researching Spoonacular API |
| Filippa | Data modeling completion *(ongoing)* |

### Blockers
None

# Sprint 3 – Standup & Status Update
**March 13, 2026**

**Attendees:** Julius, Filippa, Lisa, Rickard, Anton joined at lunch

---

## Blockers
| Who | Blocker |
|-----|---------|
| Filippa | Occupied with completion of previous course |

---

## Today
| Who     | Task |
|---------|------|
| Filippa | Continuing data modeling, will start #4 (ingredient validation) over the weekend |
| Julius | Created `init.sql` with curated schema: `curated_recipe`, `ingredients`, `recipe_ingredients`, 
`recipe_steps`, `users`, `favorites`, `search_events`, `search_event_ingredients` |
| Lisa    | Pair programming `consumer.py` and `database.py` *(Lisa driving, Rickard navigating)* |
| Anton   | Joined at lunch, briefed on sprint progress, outlined approach for Spoonacular API task |
| Rickard | Created docs folder, requested team feedback on content |
| Rickard | Added `.dockerignore` to reduce Docker image size |
| Anton | Created Pydantic schemas for Spoonacular API response – `SpoonacularRecipeInformation`, `SpoonacularIngredient`, `SpoonacularMeasures` in `app/schema/spoonacular/` |
| Anton | Created internal `Recipe` and `Ingredient` schemas in `app/schema/internal/` |


---

## Next Standup
Monday March 16 – on-site at 09:00