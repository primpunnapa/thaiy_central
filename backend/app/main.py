from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import series, studio, user, auth
from app.database.session import engine, Base
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

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

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(series.router, prefix="/api/series", tags=["Series"])
app.include_router(studio.router, prefix="/api/studios", tags=["Studio"])
app.include_router(user.router, prefix="/api/users", tags=["User"])

@app.get("/")
def root():
    return {"message": "Thai BL Central API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle business logic errors"""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "validation_error"}
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle invalid input data"""
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "type": "validation_error"}
    )

@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    """Catch any unhandled exceptions - prevents crash"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "server_error"}
    )