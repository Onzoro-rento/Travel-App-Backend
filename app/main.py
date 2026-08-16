from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import init_db, engine
import app.models  # noqa: F401
from app.exceptions.app_exceptions import AppException
from app.exceptions.handlers import app_exception_handler, validation_exception_handler
from app.routers import users, trips, trip_members, candidates, reactions, itinerary
from app.config.jwt import preload_jwks


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await preload_jwks()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]

app.include_router(users.router, prefix="/api/v1")
app.include_router(trips.router, prefix="/api/v1")
app.include_router(trip_members.router, prefix="/api/v1")
app.include_router(candidates.router, prefix="/api/v1")
app.include_router(reactions.router, prefix="/api/v1")
app.include_router(itinerary.router, prefix="/api/v1")
