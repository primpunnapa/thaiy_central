from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.database.models import Series

class SeriesRepository:
    """Handles all database operations for Series"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 20, search: Optional[str] = None, status: Optional[str] = None):
        query = self.db.query(Series)
        
        if search:
            query = query.filter(
                or_(
                    Series.title_th.contains(search),
                    Series.title_en.contains(search)
                )
            )
        
        if status:
            query = query.filter(Series.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_id(self, series_id: int):
        return self.db.query(Series).filter(Series.id == series_id).first()
    
    def create(self, series_data: dict):
        db_series = Series(**series_data)
        self.db.add(db_series)
        self.db.commit()
        self.db.refresh(db_series)
        return db_series
    
    def update(self, series_id: int, update_data: dict):
        db_series = self.get_by_id(series_id)
        if not db_series:
            return None
        
        for key, value in update_data.items():
            setattr(db_series, key, value)
        
        self.db.commit()
        self.db.refresh(db_series)
        return db_series
    
    def delete(self, series_id: int):
        db_series = self.get_by_id(series_id)
        if db_series:
            self.db.delete(db_series)
            self.db.commit()
            return True
        return False
    
    def increment_views(self, series_id: int):
        db_series = self.get_by_id(series_id)
        if db_series:
            db_series.views += 1
            self.db.commit()