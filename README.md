![FoodHub logo](images/logo.png)
## A Recipe Search Platform For All Your Needs
*Fast, easy, and surprisingly satisfying.\
Craving something good?\
***FoodHub*** turns your leftovers into something worth eating. 
Save money, cut waste, and satisfy your cravings – zero planning required.*

## 📋 Project Overview
### FoodHub is a backend API system that allows users to:
* Search for recipes by entering up to 10 ingredients
* Get at least 3 recipe suggestions ranked by number of matching ingredients
* Save favourite recipes
* Get random recipe suggestions

## 🛠️ Tech Stack

- **API** – FastAPI (Python)
- **Messaging** – Apache Kafka
- **Database** – PostgreSQL
- **Containerization** – Docker / docker-compose
- **Data processing** – Pandas
- **Package manager** – uv

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

4. API is now running at `http://localhost:8000`

5. Test in postgreSQL:
docker exec -i postgres psql -U foodhub -d foodhub_db < init.sql
docker exec -it postgres psql -U foodhub -d foodhub_db -c "SELECT * FROM staging_recipes;"

## 👀 Behind the scenes - add separate pdf:s
- The Team Work (planing poker, agile roles etc)
- Data Modeling and business requirements 
