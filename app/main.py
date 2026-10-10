from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routes.certificates import router as certificates_router
from app.routes.jobs import router as jobs_router

# Import models so SQLAlchemy registers all table definitions.
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Bulk Certificate Generator",
    description=(
        "Create bulk certificate jobs, monitor progress, "
        "and retrieve generated PDF certificates."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(jobs_router)
app.include_router(certificates_router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
