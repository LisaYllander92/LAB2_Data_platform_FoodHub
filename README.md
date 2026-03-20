![FoodHub logo](images/logo.png)
## A Recipe Search Platform For All Your Needs
*Fast, easy, and surprisingly satisfying.\
Craving something good?\
***FoodHub*** turns your leftovers into something worth eating. 
Save money, cut waste, and satisfy your cravings – zero planning required.*
---
## 📋 Project Overview
### FoodHub is a robust data platform and backend API designed to bridge the gap between raw ingredients and delicious meals. It features:
* **Smart Search:** Search for recipes by entering up to 10 ingredients.
* **Fuzzy Matching:** Handles typos and misspellings (e.g., "avocdo" -> "avocado") using Levenshtein distance.
* **Ranking Logic:** Recipe suggestions are ranked by the number of matching ingredients.
* **Persistent Storage:** Save favorite recipes and access random suggestions.

## 🏗️ Architecture & Data Flow
The system follows a modern **Data Engineering** pipeline to ensure data quality and scalability:

1. **Ingestion (The Producer):** FastAPI acts as the Producer. It fetches recipe data from the Spoonacular API and pushes the results as events into a Kafka topic.
2. **Streaming:** ***Apache Kafka*** acts as the central broker, safely buffering these search results as asynchronous JSON payloads.
3. **Processing (The Consumer)**: A dedicated ***Kafka Consumer*** service listens to the stream. It performs the "heavy lifting": validating data types and executing ***Regex transformations***  to strip HTML metadata from recipe instructions.
4. **Storage (Medallion Architecture):** The Consumer then persists the data into two distinct layers:
    - `staging_recipes`: Stores raw JSON payloads for historical auditing and backup.
    - `curated_recipe`: Stores cleaned, structured, and relational data ready for the frontend.


### 💻 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![RapidFuzz](https://img.shields.io/badge/RapidFuzz-3776AB?style=for-the-badge&logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-de5b41?style=for-the-badge&logo=uv&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
---

## 🚀 Getting Started
### Prerequisites
* Python 3.12
* Docker Desktop
* uv – [install here](https://docs.astral.sh/uv/getting-started/installation/)

### Installation

1. Clone the repository
```bash
git clone https://github.com/LisaYllander92/LAB2_Data_platform_FoodHub.git
cd LAB2_Data_platform_FoodHub
```

2. Install dependencies
```bash
uv sync
```

3. Start all services
```bash
docker compose up --build
```

4. Access the API:
The interactive API documentation (Swagger) is available at http://localhost:8000/docs

## 🧪 Database Access & Verification 
Use these commands to explore the database or verify that the data pipeline is working correctly.

### 1. Manual Access (PostgreSQL CLI)
```bash
docker exec -it postgres psql -U foodhub -d foodhub_db
```
*Once inside, use \dt to list tables or \q to exit.*

### 2. Schema Reset
*If you need to manually re-run the initialization script:*
```bash
docker exec -i postgres psql -U foodhub -d foodhub_db < init.sql
```

### 3. Quick Verification (Direct Commands)
*Run these directly in your terminal to verify the ETL process and Data Transformation:*

**Check Raw Data (Staging count):**\
*Verifies that the Kafka Consumer is successfully saving every incoming message.*
```bash
docker exec -it postgres psql -U foodhub -d foodhub_db -c "SELECT count(*) AS total_raw_recipes FROM staging_recipes;"
```
**View Cleaned Data (Curated table):**\
*Verifies that the Regex transformation has stripped HTML tags and structured the data.*
```bash
docker exec -it postgres psql -U foodhub -d foodhub_db -c "SELECT id, title, servings, LEFT(instructions, 60) || '...' AS cleaned_instructions FROM curated_recipes LIMIT 5;"
```
---
## 👀 Behind the scenes 
*Detailed documentation of our architectural design and agile development process:*


### 📊 Data Modeling
*Click the links below to view our models:*
- [Conceptual Model](docs/Conceptual_model.png)
- [Logical Model](docs/Logical_model.png)

### 🔄 Agile Process & Logs
**Sprint 1**
- [Activity Log](docs/sprint1_activity_log.md)
- [Retrospective](docs/sprint1_retrospective.md)

**Sprint 2**
- [Activity Log](docs/sprint2_activity_log.md)
- [Retrospective](docs/sprint2_retrospective.md)

**Sprint 3**
- [Activity Log](docs/sprint3_activity_log.md)
- [Retrospective](docs/sprint3_retrospective.md)