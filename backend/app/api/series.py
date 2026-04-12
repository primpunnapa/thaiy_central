from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.database.models import User
from app.persistence.series import SeriesRepository
from app.persistence.studio import StudioRepository
from app.business.series import SeriesService
from app.schemas.series import Series, SeriesCreate, SeriesUpdate, SeriesList, SeriesSchedule
from app.core.auth import require_active_user, require_editor

router = APIRouter()

def get_series_service(db: Session = Depends(get_db)):
    series_repo = SeriesRepository(db)
    studio_repo = StudioRepository(db)
    return SeriesService(series_repo, studio_repo)

# Normal users can access
@router.get("/", response_model=List[SeriesList])
def get_series(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    service: SeriesService = Depends(get_series_service)
):
    """Get all series - Public access"""
    return service.get_all_series(skip, limit, search, status)

@router.get("/schedule", response_model=SeriesSchedule)
def get_schedule(service: SeriesService = Depends(get_series_service)):
    """Get schedule grouped by day of week - Public access"""
    return service.get_schedule()

@router.get("/{series_id}", response_model=Series)
def get_series_detail(
    series_id: int,
    service: SeriesService = Depends(get_series_service)
):
    """Get series details - Public access"""
    series = service.get_series_detail(series_id)
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")
    return series

# Editor only
@router.post("/", response_model=Series, status_code=201)
def create_series(
    series: SeriesCreate,
    service: SeriesService = Depends(get_series_service),
    current_user: User = Depends(require_editor)  # Create permission
):
    """Create new series - Editor only"""
    try:
        return service.create_series(series)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{series_id}", response_model=Series)
def update_series(
    series_id: int,
    series_update: SeriesUpdate,
    service: SeriesService = Depends(get_series_service),
    current_user: User = Depends(require_editor)  # Update permission
):
    """Update series - Editor only"""
    updated = service.update_series(series_id, series_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Series not found")
    return updated

@router.delete("/{series_id}", status_code=204)
def delete_series(
    series_id: int,
    service: SeriesService = Depends(get_series_service),
    current_user: User = Depends(require_editor)  # Delete permission
):
    """Delete series - Editor only"""
    deleted = service.delete_series(series_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Series not found")
    return None