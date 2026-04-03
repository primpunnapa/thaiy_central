from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.persistence.studio import StudioRepository
from app.business.studio import StudioService
from app.schemas.studio import Studio, StudioCreate

router = APIRouter()

def get_studio_service(db: Session = Depends(get_db)):
    studio_repo = StudioRepository(db)
    return StudioService(studio_repo)

@router.get("/", response_model=List[Studio])
def get_studios(service: StudioService = Depends(get_studio_service)):
    return service.get_all_studios()

@router.post("/", response_model=Studio, status_code=201)
def create_studio(
    studio: StudioCreate,
    service: StudioService = Depends(get_studio_service)
):
    try:
        return service.create_studio(studio)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))