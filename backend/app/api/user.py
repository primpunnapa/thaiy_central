from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.database.models import User as UserModel
from app.persistence.user import UserRepository
from app.business.user import UserService
from app.schemas.user import UserCreate
from app.schemas.auth import UserResponse, UserUpdate
from app.core.auth import require_admin

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    return UserService(user_repo)

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: UserService = Depends(get_user_service),
    admin: UserModel = Depends(require_admin)
):
    """Get all users (Admin only)"""
    return service.get_all_users(skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    admin: UserModel = Depends(require_admin)
):
    """Get specific user (Admin only)"""
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
    admin: UserModel = Depends(require_admin)
):
    """Create new user (Admin only)"""
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service),
    admin: UserModel = Depends(require_admin)
):
    """Update user (Admin only)"""
    try:
        return service.update_user(user_id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    admin: UserModel = Depends(require_admin)
):
    """Delete user (Admin only)"""
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))