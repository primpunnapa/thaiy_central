from app.persistence.user import UserRepository
from app.schemas.user import UserCreate

class UserService:
    """Contains business logic for Users"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.user_repo.get_all(skip, limit)
    
    def get_user(self, user_id: int):
        return self.user_repo.get_by_id(user_id)
    
    def create_user(self, user_data: UserCreate):
        # Check if username exists
        existing = self.user_repo.get_by_username(user_data.username)
        if existing:
            raise ValueError(f"Username {user_data.username} already exists")
        
        return self.user_repo.create(user_data.model_dump())