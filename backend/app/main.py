from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import series, studios, users
from app.core.database import engine, Base

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
app.include_router(studios.router, prefix="/api/studios", tags=["Studios"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Thai BL Central API"}

@app.get("/health")
def health():
    return {"status": "ok"}