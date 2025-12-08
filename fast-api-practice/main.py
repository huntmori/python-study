from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users
from app.routers import chat


app = FastAPI(
    title="FastAPI JWT Authentication",
    description="FastAPI project with JWT authentication, MariaDB, and SQLAlchemy 2.0",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(chat.router)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        print("The API will start, but database operations may fail.")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastAPI JWT Authentication API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
