from app.persistence.user import UserRepository
from app.schemas.auth import LoginResponse, UserResponse, UserCreate
from app.core.auth import create_access_token, get_password_hash, verify_password


class AuthService:
    """Contains business logic for Authentication"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def login(self, username: str, password: str) -> LoginResponse:
        """Authenticate user and return access token"""
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password) or not user.is_active:
            raise ValueError("Incorrect username or password")
        
        # Update last login via repository
        from datetime import datetime, timezone
        user_data = {"last_login": datetime.now(timezone.utc)}
        user = self.user_repo.update(user.id, user_data)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.username})
        
        return LoginResponse(
            access_token=access_token,
            user=UserResponse.model_validate(user)
        )
    
    def register(self, user_data: UserCreate) -> UserResponse:
        """Register new user (normal users only)"""
        # Check if username exists
        existing = self.user_repo.get_by_username(user_data.username)
        if existing:
            raise ValueError("Username already taken")
        
        # Check if email exists
        existing_email = self.user_repo.get_by_email(user_data.email)
        if existing_email:
            raise ValueError("Email already registered")
        
        # Force role to NORMAL for self-registration
        from app.database.models import UserRole
        new_user_data = {
            "username": user_data.username,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": get_password_hash(user_data.password),
            "role": UserRole.NORMAL
        }
        
        new_user = self.user_repo.create(new_user_data)
        return UserResponse.model_validate(new_user)
