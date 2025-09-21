from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .config import settings
from .routers import auth as auth_router, products as products_router, tokens as tokens_router

app = FastAPI(title="Charity App (FastAPI)")

# configures and initializes a FastAPI application with CORS, database setup and route registration
# processes the CORS_ORIGINS setting, which expects to be a comma-seperated string of allowed domains
# splits the string by commas, strips any whitespace and filters empty strings
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
# following setup is used to enable secure communication between the backend and frontend running on different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# each router organizes related endpoints, making the API modular and better to maintain
init_db()
app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(tokens_router.router)