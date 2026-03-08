import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth, posts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Darkvus Portfolio API",
    description="Blog API for darkvus.dev portfolio",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:4173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
