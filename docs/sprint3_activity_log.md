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
| Anton | Implemented generic async `HttpClient` using `httpx` with Pydantic model validation |


---

# Sprint 3 – Standup & Status Update
**March 16, 2026**

**Attendees:** Julius, Filippa, Lisa, Rickard. Anton joined via call (sick).

---

## Today
| Who     | Task |
|---------|------|
| Team    | Full sync to check status and align the group. |
| Lisa    | **Lead Developer:** Responsible for the majority of code implementation during the session. |
| Filippa | Data modeling completed. Now transitioning to full-time focus on group tasks. |
| Anton   | Participated via call (sick). Briefed the team on Friday's progress and implementation. |
| Team    | Code review: Walkthrough of Anton's code to ensure shared understanding. |
| Team    | Troubleshooting: Extensive debugging session led by Lisa to resolve system issues. |
| Team    | API Management: Configured an additional API key after reaching the token limit. |
| Team    | Started development of `ingredient_validator`. |
| Team    | Integration testing: Verified the Producer-Topic-Consumer flow with success. |

---

## Blockers
| Who | Blocker |
|-----|---------|
| Anton | Out sick (participated remotely for sync and troubleshooting). |
| Team  | Reached token limit for API (resolved by adding a new API key). |

---

## Delivered
| Who    | Delivery |
|--------|----------|
| Lisa   | Implementation of core logic and bug fixes across the system. |
| Filippa| Finalized Data Modeling. |
| Team   | Successful end-to-end test of the Kafka pipeline (Producer -> Topic -> Consumer). |

---

## Next Standup
Tuesday March 17 – 09:00