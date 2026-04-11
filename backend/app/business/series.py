from typing import Optional, List
from app.persistence.series import SeriesRepository
from app.persistence.studio import StudioRepository
from app.schemas.series import SeriesCreate, SeriesUpdate

class SeriesService:
    """Contains business logic for Series"""
    
    def __init__(self, series_repo: SeriesRepository, studio_repo: StudioRepository):
        self.series_repo = series_repo
        self.studio_repo = studio_repo
    
    def get_all_series(self, skip: int = 0, limit: int = 20, search: Optional[str] = None, status: Optional[str] = None):
        return self.series_repo.get_all(skip, limit, search, status)
    
    def get_series_detail(self, series_id: int):
        series = self.series_repo.get_by_id(series_id)
        if series:
            self.series_repo.increment_views(series_id)
        return series
    
    def create_series(self, series_data: SeriesCreate):
        if series_data.release_year and series_data.release_year > 2026:
            raise ValueError("Release year cannot be in the future")
        
        return self.series_repo.create(series_data.model_dump())
    
    def update_series(self, series_id: int, series_data: SeriesUpdate):
        return self.series_repo.update(
            series_id,
            series_data.model_dump(exclude_unset=True)
        )
    
    def delete_series(self, series_id: int):
        return self.series_repo.delete(series_id)
    
    def get_schedule(self):
        """Get all series with schedule info grouped by day of the week"""
        all_series = self.series_repo.get_all(limit=100)
        series_with_schedule = [s for s in all_series if s.air_day and s.air_time]
        
        # Initialize schedule dict with all days
        schedule = {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
            "saturday": [],
            "sunday": []
        }
        
        # Group series by day (case-insensitive)
        for series in series_with_schedule:
            day = series.air_day.lower() if series.air_day else None
            if day in schedule:
                schedule[day].append(series)
        
        # Sort each day's series by air_time
        for day in schedule:
            schedule[day].sort(key=lambda s: s.air_time or "")
        
        return schedule