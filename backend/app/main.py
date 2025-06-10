from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.core.database import engine
from app.models import content
import os

# Create tables
content.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Golden Compass API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(routes.router, prefix="/api")

# Static files
if os.path.exists("media"):
    app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
async def root():
    return {"message": "Golden Compass API is running"}