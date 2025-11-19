import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import Base, engine

from app.routers.upload import router as upload_router
from app.routers.progress import router as progress_router
from app.routers.products import router as products_router
from app.routers.webhooks import router as webhooks_router
from app.routers.delete_all import router as delete_all_router

app = FastAPI(title="Product Importer")

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Serve HTML templates & static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(delete_all_router)
app.include_router(products_router)
app.include_router(upload_router)
app.include_router(progress_router)
app.include_router(webhooks_router)

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.get("/webhooks-page")
def webhooks_page(request: Request):
    return templates.TemplateResponse("webhooks.html", {"request": request})


@app.get("/products-page")
def products_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})
