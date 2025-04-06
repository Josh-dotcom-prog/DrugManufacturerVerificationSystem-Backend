from fastapi import APIRouter, Depends, status

from app.services.batches import BatchService
from app.repository.batches import BatchesRepository
from app.schemas.batches import *
from app.responses.batches import *
from app.repository.manufacturer import ManufacturerRepository

from sqlalchemy.orm import Session

from app.database.database import get_session
from app.core.security import Security

from typing import List

security = Security()

batch_router = APIRouter(
    prefix="/batch",
    tags=["Manufacturer Batch"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(security.oauth2_scheme), Depends(security.get_current_user)]
)

def get_batch_service(session: Session = Depends(get_session)) -> BatchService:
    batch_repository = BatchesRepository(session)
    manufacturer_repository = ManufacturerRepository(session)
    return BatchService(batch_repository, manufacturer_repository)

@batch_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=BatchResponse)
async def create_batch(data: BatchCreate, current_user = Depends(security.get_current_user),
                       batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.create_batch(data, current_user)

@batch_router.put("/update", status_code=status.HTTP_200_OK, response_model=BatchResponse)
async def update_batch(data: BatchUpdate, current_user = Depends(security.get_current_user),
                       batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.update_batch(data, current_user)

@batch_router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_batch(batch_id: int, current_user = Depends(security.get_current_user),
                       batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.delete_batch(batch_id, current_user)

@batch_router.get("/batch", status_code=status.HTTP_200_OK, response_model=BatchResponse)
async def get_batch_by_id(batch_id: int, current_user = Depends(security.get_current_user),
                          batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.get_batch_by_id(batch_id, current_user)

@batch_router.get("/batches", status_code=status.HTTP_200_OK, response_model=List[BatchResponse])
async def get_all_my_batches(current_user= Depends(security.get_current_user),
                             batch_service: BatchService = Depends(get_batch_service)):
    return await batch_service.get_all_batches(current_user)