from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User
from app.persistence.user import UserRepository
from app.business.auth import AuthService
from app.schemas.auth import LoginRequest, LoginResponse, UserCreate, UserResponse
from app.core.auth import get_current_user

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)):
    """Service factory - API instantiates Repository and passes to Service"""
    user_repo = UserRepository(db)
    return AuthService(user_repo)

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    """Login and get access token"""
    try:
        return service.login(request.username, request.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """Logout (client-side token discard)"""
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, service: AuthService = Depends(get_auth_service)):
    """Register new user (normal users only)"""
    try:
        return service.register(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))