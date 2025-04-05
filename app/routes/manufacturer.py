from fastapi import APIRouter, status, Depends


from app.services.manufacture import ManufacturerService
from app.repository.manufacturer import ManufacturerRepository
from app.responses.manufacturer import *
from app.schemas.manufacturer import *

from app.core.config import get_settings
from app.core.security import Security
from app.database.database import get_session

from sqlalchemy.orm import Session

security = Security()



manufacturer_router = APIRouter(
    prefix="/manufacturer",
    tags=["Manufacturer"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(security.oauth2_scheme), Depends(security.get_current_user)]
)


def get_manufacturer_service(session: Session = Depends(get_session)) -> ManufacturerService:
    manufacturer_repository = ManufacturerRepository(session)
    return ManufacturerService(manufacturer_repository)

@manufacturer_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_manufacturer(data: ManufacturerCreate, current_user = Depends(security.get_current_user),
                              manufacturer_service: ManufacturerService = Depends(get_manufacturer_service)):
    return await manufacturer_service.create_manufacturer(current_user, data)