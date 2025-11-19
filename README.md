# Product Importer – FastAPI + Celery + Redis

A backend system that supports **large CSV product imports**, background processing, progress tracking, and full product management through a simple web interface.

---

## Tech Stack

- **FastAPI** — Web API framework  
- **Celery** — Async background task queue  
- **Redis** — Message broker + progress storage  
- **PostgreSQL** — Database  
- **SQLAlchemy** — ORM  
- **Jinja2 + HTML/JS** — Frontend templates  

---

## How to Run the Project (Local Setup)

### 1 Clone the repository
```sh
git clone <repo-url>
cd product-importer
```
### 2 Create a virtual environment (Windows)
```sh
python -m venv venv
venv\Scripts\activate   
```
### 3 Install dependencies
```sh
pip install -r requirements.txt
```
### 4 Create .env file in project root like this (this is my .env, it won't work in yours, so keep it similar to this)
```sh
DATABASE_URL = postgresql://postgres:lylGpRTcbmuwBeGEutusDSePSSzEjAyZ@postgres.railway.internal:5432/railway
REDIS_URL = redis://default:FYCOZdQ4Ls4IVSomBo2lAHIzPzXZkqmQ@redis-19529.c301.ap-south-1-1.ec2.cloud.redislabs.com:19529
SECRET_KEY = mysecret123
UPLOAD_DIR = uploads
```
### 5 Setup PostgreSQL database
```sh
psql -U postgres
CREATE DATABASE product_importer;
```
### 6 Start Redis
```sh
redis-server
```
### 7 Start Celery worker
```sh
celery -A app.workers.celery_app worker --loglevel=info --pool=solo
```
### 8 Start FastAPI server
```sh
uvicorn app.main:app --reload
```
### 9 Deployed project
```sh
https://product-importer-production-5616.up.railway.app/
```

Note - 
It is deployed on the Railway platform
In my code, I save the uploaded CSV in a folder and then use it for celery and other places where the CSV is required. But, since the Railway deployment platform free version doesn't support the use of shared volume, the deployed project won't work 100%. So, for 100% working, please run locally in your system for perfect output, i.e the use of celery and redis in my project.
