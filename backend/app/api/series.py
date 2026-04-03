from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.persistence.series import SeriesRepository
from app.persistence.studio import StudioRepository
from app.business.series import SeriesService
from app.schemas.series import Series, SeriesCreate, SeriesUpdate, SeriesList

router = APIRouter()

def get_series_service(db: Session = Depends(get_db)):
    series_repo = SeriesRepository(db)
    studio_repo = StudioRepository(db)
    return SeriesService(series_repo, studio_repo)

@router.get("/", response_model=List[SeriesList])
def get_series(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    service: SeriesService = Depends(get_series_service)
):
    """Get all series with filters"""
    return service.get_all_series(skip, limit, search, status)

@router.get("/schedule", response_model=List[SeriesList])
def get_schedule(service: SeriesService = Depends(get_series_service)):
    """Get all series with schedule info"""
    return service.get_schedule()

@router.get("/{series_id}", response_model=Series)
def get_series_detail(
    series_id: int,
    service: SeriesService = Depends(get_series_service)
):
    """Get series by ID"""
    series = service.get_series_detail(series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series

@router.post("/", response_model=Series, status_code=201)
def create_series(
    series: SeriesCreate,
    service: SeriesService = Depends(get_series_service)
):
    """Create new series"""
    try:
        return service.create_series(series)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{series_id}", response_model=Series)
def update_series(
    series_id: int,
    series_update: SeriesUpdate,
    service: SeriesService = Depends(get_series_service)
):
    """Update series"""
    updated = service.update_series(series_id, series_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Series not found")
    return updated

@router.delete("/{series_id}", status_code=204)
def delete_series(
    series_id: int,
    service: SeriesService = Depends(get_series_service)
):
    """Delete series"""
    deleted = service.delete_series(series_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Series not found")
    return None