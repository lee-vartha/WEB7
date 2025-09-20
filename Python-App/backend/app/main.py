from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .config import settings
from .routers import auth as auth_router, products as products_router, tokens as tokens_router

app = FastAPI(title="Charity App (FastAPI)")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(tokens_router.router)