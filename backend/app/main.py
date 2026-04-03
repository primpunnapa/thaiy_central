from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import series, studio, user  # Changed from 'studio' to 'studios'
from app.database.session import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Thai BL Central")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(series.router, prefix="/api/series", tags=["Series"])
app.include_router(studio.router, prefix="/api/studios", tags=["Studio"])
app.include_router(user.router, prefix="/api/users", tags=["User"])

@app.get("/")
def root():
    return {"message": "Thai BL Central API"}

@app.get("/health")
def health():
    return {"status": "ok"}