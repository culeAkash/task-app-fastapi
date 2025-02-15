from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError,HTTPException
from app.routes import notes
from app.exceptions import validation_exception_handler, http_exception_handler
from contextlib import asynccontextmanager
from app.database import create_indexes


#create indexes on startup

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_indexes()
    yield
    
app = FastAPI(lifespan=lifespan)


# Include routers

app.include_router(notes.router,prefix="/notes",tags=["notes"])




#exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/")
async def root():
    return {"message": "Welcome to the Notes API"}