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
    
    def delete_studio(self, studio_id: int):
        studio = self.studio_repo.get_by_id(studio_id)
        if not studio:
            raise ValueError(f"Studio with id {studio_id} not found")
        
        self.studio_repo.db.delete(studio)
        self.studio_repo.db.commit()
    
    def update_studio(self, studio_id: int, studio_data: StudioCreate):
        studio = self.studio_repo.get_by_id(studio_id)
        if not studio:
            raise ValueError(f"Studio with id {studio_id} not found")
        
        update_data = studio_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(studio, key, value)
        
        self.studio_repo.db.commit()
        self.studio_repo.db.refresh(studio)
        return studio