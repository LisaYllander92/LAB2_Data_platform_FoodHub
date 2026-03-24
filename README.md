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
* **Fuzzy Matching:** Handles smaller typos and misspellings (e.g., "avocdo" -> "avocado") using RapidFuzz.
* **Ranking Logic:** Recipe suggestions are ranked by the number of matching ingredients.
* **Cache-First Strategy:** Checks the database before calling the Spoonacular API to minimize API costs.
* **Search Statistics:** Tracks and visualizes the most popular ingredient searches using Matplotlib.
* **Frontend:** A lightweight web interface for searching recipes and viewing history.

---

## 🏗️ Architecture & Data Flow
The system follows a modern **Data Engineering** pipeline to ensure data quality and scalability:

1. **Ingestion (The Producer):** FastAPI acts as the Producer. It fetches recipe data from the Spoonacular API and pushes the results as events into a Kafka topic.
2. **Streaming:** ***Apache Kafka*** acts as the central broker, safely buffering these search results as asynchronous JSON payloads.
3. **Processing (The Consumer):** A dedicated ***Kafka Consumer*** service listens to the stream. It validates data types and saves raw payloads to the staging layer.
4. **Storage (Medallion Architecture):** Data is persisted into two distinct layers in **Supabase (PostgreSQL)**:
    - `staging_recipes`: Stores raw JSON payloads for historical auditing and backup.
    - `curated_recipes`: Stores cleaned, structured, and validated data ready for the frontend.
5. **Statistics:** Search queries are logged in `search_log` and visualized as bar charts via Matplotlib.

---

## 💻 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![RapidFuzz](https://img.shields.io/badge/RapidFuzz-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-de5b41?style=for-the-badge&logo=uv&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
---

## 🚀 Getting Started
### Prerequisites
* Python 3.12
* Docker Desktop
* uv – [install here](https://docs.astral.sh/uv/getting-started/installation/)
* A Supabase account and project – [get started here](https://supabase.com)

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
3. Set up your `.env` file with your Supabase credentials:
```env
DB_HOST=your-db-host
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-supabase-password
SPOONACULAR_API_KEY=your-api-key
SPOONACULAR_USERNAME=your-spoonacular-username
SPOONACULAR_HASH=your-spoonacular-hash
```
4. Initialize the database schema in Supabase by running `init.sql` in the Supabase SQL editor.
5. Start all services
```bash
docker compose up --build
```
6. Access the app:
- **Frontend:** http://localhost:8000
- **API docs (Swagger):** http://localhost:8000/docs
- **Kafka UI:** http://localhost:8080
- **Search statistics plot:** http://localhost:8000/api/recipes/stats/plot
---
## 📊 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/recipes/search` | Search recipes by ingredients |
| GET | `/api/recipes/detail/{title}` | Get full recipe details |
| GET | `/api/recipes/history` | View recently saved recipes |
| GET | `/api/recipes/popular-searches` | Top 10 most searched ingredients |
| GET | `/api/recipes/stats/plot` | Bar chart of popular searches |
| POST | `/api/recipes` | Send a recipe to Kafka |

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