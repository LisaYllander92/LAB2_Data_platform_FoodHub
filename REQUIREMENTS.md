# REQUIREMENTS.md – FoodHub

## Purpose

FoodHub is a recipe suggestion application that helps users find recipes based on ingredients they already have at home. The goal is to reduce food waste, save money, and make it easier for people who are unsure what to cook.

---

## Target Audience

- People who do not know what to cook
- People who are not confident in the kitchen
- People who want to use ingredients they already have at home
- People who want to save money by reducing food waste

---

## MVP (Minimum Viable Product)

The core functionality required for a working product:

- User can enter ingredients they have at home
- User receives recipe suggestions based on those ingredients
- Recipes are ranked by number of matching ingredients
- Each recipe displays cleaned & validated: ingredients, instructions, cooking time, and number of servings

---

## User Stories

| ID  | Description |
|-----|-------------|
| #7  | As a user I want to see how well a recipe matches my ingredients so that I can choose among the recipes with the most matches |
| #8  | As a developer I want to set up a connection to the Spoonacular API so that we can fetch recipe data to use in our pipeline |
| #9  | As a system I want to consume Kafka messages and store raw data in a staging table in PostgreSQL so that data can be validated and transformed before being moved to production tables |
| #11 | As a developer I want a FastAPI endpoint that returns matched recipes so that we can easily retrieve more suggestions from already existing recipes |
| #12 | As a team we want to demonstrate a working pipeline from API -> Kafka -> DB -> FastAPI in the sprint demo so that we know it works |
| #13 | As a developer I want a clear overview of the project so that I can quickly see how the different parts connect |
| #14 | As a customer I want a clear requirements specification that mirrors the ERD so that it is clear what is expected |
| #15 | As a user I want to get multiple recipe suggestions so that I can choose what to cook |
| #16 | As a developer I want to clean and sanitize data before it reaches the user so that the recipes that reach the user are correct |
| #17 | As a developer I want the user to be able to type misspelled ingredients and still get recipe suggestions |
| #26 | Set up Kafka topic configuration in Docker Compose so that messages can be sent and consumed with transaction history |
| #29 | As a system I want to transform and validate data from the staging table and move it to a curated table so that only correct and consistent data is used when users search for recipes |
| #34 | As a developer I want all database tables to be defined in init.sql and mirror the logical model |
| #41 | As a user I want to see recipe history of my previously searched recipes so that I can easily cook them again |
| #47 | As a developer I want to use caching so that recipes are saved in curated_recipe and I do not need to worry about token usage |
| #48 | As a developer I want to see statistics on users' most popular searches so that future recipe suggestions can be adapted |
| #49 | As a user I want a easy to navigate application so that I can use the service easily |
| #50 | As a developer I want to ensure that recipe suggestions shown from curated are clean |
| #51 | As a user I want all ingredients in a neat list so that the recipe is easier to read |
| #58 | Bug fix: progression bar in frontend for amount of matching ingredients lacks proper validation |
| #61 | As a developer I want the same data in the database as my fellow developers so that all searched ingredients are saved regardless of developer |

---

## Functional Requirements

### Core
- Users can input up to 10 ingredients per search
- The system suggests recipes based on the input
- Recipes are ranked by number of matching ingredients
- Each recipe must include: ingredients, instructions, cooking time, servings
- Search history is stored and viewable
- Statistics displaying most popular ingredient searches
- Recipe images

---

## Non-Functional Requirements

- The system uses a cache-first strategy (curated table before Spoonacular API) to minimize API costs
- All code, comments, variable names, and documentation are written in English
- Variables use snake_case naming convention
- The application runs via Docker Compose

---

## Technical Requirements

| Component        | Technology                  |
|------------------|-----------------------------|
| Backend          | FastAPI (Python)            |
| Database         | PostgreSQL (Supabase)       |
| Message broker   | Apache Kafka                |
| Data processing  | Pandas, RapidFuzz           |
| External API     | Spoonacular                 |
| Frontend         | HTML, CSS, JavaScript       |
| Containerization | Docker / Docker Compose     |
| DB pool          | psycopg_pool                |
| Validation       | Pydantic                    |
| Visualization    | Matplotlib                  |
| Package manager  | uv                          |
| Cache strategy   | Cache-first (curated_recipes) |

---

## Definition of Done

A user story is considered done when:

- [ ] Code is tested and works in the `development` branch
- [ ] Code follows the project coding standard
- [ ] The team has reviewed and approved the code
- [ ] Code is pushed to the correct branch
- [ ] Pull Request is created and reviewed

---

## Coding Standard

- Commit messages: `feat: description`, `add: description`, `update: description`, `fix: description`
- All code, variables, comments, and docs written in English
- Variable names use snake_case
- New names are agreed upon with the team before use
- No code is pushed after sprint deadline
