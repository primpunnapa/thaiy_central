from sqlalchemy.orm import Session
from app.database.models import Studio

class StudioRepository:
    """Handles all database operations for Studios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Studio).all()
    
    def get_by_id(self, studio_id: int):
        return self.db.query(Studio).filter(Studio.id == studio_id).first()
    
    def create(self, studio_data: dict):
        db_studio = Studio(**studio_data)
        self.db.add(db_studio)
        self.db.commit()
        self.db.refresh(db_studio)
        return db_studio
    
    def get_or_create_by_name(self, name: str):
        studio = self.db.query(Studio).filter(Studio.name == name).first()
        if not studio:
            studio = Studio(name=name)
            self.db.add(studio)
            self.db.commit()
            self.db.refresh(studio)
        return studio