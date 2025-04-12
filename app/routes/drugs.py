from fastapi import APIRouter, HTTPException, status, Depends

from app.services.drugs import DrugService
from app.repository.drugs import DrugRepository
from app.schemas.drugs import *
from app.responses.drugs import *

from app.repository.manufacturer import ManufacturerRepository
from app.repository.batches import BatchesRepository

from typing import List

from sqlalchemy.orm import Session

from app.database.database import get_session

from app.core.security import Security

security = Security()

drug_router = APIRouter(
    prefix="/drug",
    tags=["Manufacturer Drug"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(security.oauth2_scheme), Depends(security.get_current_user)]
)

def get_drug_service(session: Session = Depends(get_session)) -> DrugService:
    drug_repository = DrugRepository(session)
    batch_repository = BatchesRepository(session)
    manufacturer_repository = ManufacturerRepository(session)
    return DrugService(drug_repository, batch_repository, manufacturer_repository)

@drug_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=DrugResponse)
async def create_drug(data: DrugCreate, current_user = Depends(security.get_current_user),
                      drug_service: DrugService = Depends(get_drug_service)):
    return await drug_service.create_drug(data, current_user)

@drug_router.put("/update", status_code=status.HTTP_200_OK, response_model=DrugResponse)
async def update_drug(data: DrugUpdate, current_user = Depends(security.get_current_user),
                      drug_service: DrugService = Depends(get_drug_service)):
    return await drug_service.update_drug(data, current_user)

@drug_router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_drug(drug_id: int, current_user = Depends(security.get_current_user),
                      drug_service: DrugService = Depends(get_drug_service)):
    return await drug_service.delete_drug(drug_id, current_user)

@drug_router.get("/drug", status_code=status.HTTP_200_OK, response_model=List[DrugResponse])
async def get_all_my_drugs(current_user = Depends(security.get_current_user),
                           drug_service: DrugService = Depends(get_drug_service)):
    return await drug_service.get_all_my_drugs(current_user)

