from app.persistence.studio import StudioRepository
from app.schemas.studio import StudioCreate

class StudioService:
    """Contains business logic for Studios"""
    
    def __init__(self, studio_repo: StudioRepository):
        self.studio_repo = studio_repo
    
    def get_all_studios(self):
        return self.studio_repo.get_all()
    
    def create_studio(self, studio_data: StudioCreate):
        # Check if studio already exists
        existing = self.studio_repo.get_by_id(studio_data.id) if hasattr(studio_data, 'id') else None
        if existing:
            raise ValueError(f"Studio with id {studio_data.id} already exists")
        
        return self.studio_repo.create(studio_data.model_dump())