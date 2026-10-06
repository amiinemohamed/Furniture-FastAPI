from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import router as api_router
from app.web import router as web_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Furniture price prediction",
    description="Web interface and API gateway for furniture price predictions.",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(web_router)
app.include_router(api_router, tags=["predictions"])
