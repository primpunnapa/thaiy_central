from app.persistence.user import UserRepository
from app.schemas.user import UserCreate
from app.core.auth import get_password_hash

class UserService:
    """Contains business logic for Users"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.user_repo.get_all(skip, limit)
    
    def get_user(self, user_id: int):
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_username(self, username: str):
        return self.user_repo.get_by_username(username)
    
    def create_user(self, user_data: UserCreate):
        # Check if username exists
        existing = self.user_repo.get_by_username(user_data.username)
        if existing:
            raise ValueError(f"Username {user_data.username} already exists")
        
        # Check if email exists
        existing_email = self.user_repo.get_by_email(user_data.email)
        if existing_email:
            raise ValueError(f"Email {user_data.email} already registered")
        
        # Create user with hashed password
        user_dict = user_data.model_dump()
        user_dict['hashed_password'] = get_password_hash(user_dict.pop('password', ''))
        return self.user_repo.create(user_dict)
    
    def update_user(self, user_id: int, user_data):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        # Convert Pydantic model to dict if needed
        if hasattr(user_data, 'model_dump'):
            user_data = user_data.model_dump(exclude_unset=True)
        else:
            user_data = dict(user_data)
        
        # Hash password if provided
        if 'password' in user_data and user_data['password']:
            user_data['hashed_password'] = get_password_hash(user_data.pop('password'))
        else:
            user_data.pop('password', None)
        
        return self.user_repo.update(user_id, user_data)
    
    def delete_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        self.user_repo.delete(user_id)
        return True