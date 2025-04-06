from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.drugs import Drug
from app.repository.drugs import DrugRepository
from app.schemas.drugs import *
from app.responses.drugs import *

from app.models.users import User, UserRole

from datetime import datetime


class DrugService:
    def __init__(self, drug_repository: DrugRepository):
        self.drug_repository = drug_repository

    async  def create_drug(self, data: DrugCreate, current_user: User) -> DrugResponse:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a manufacture to access this route.")

        drug_exists = self.drug_repository.get_drug_by_name(data.name)
        if drug_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this name already exists.")

        # Proceed to create the drug
        drug_to_create = Drug(
            serial_number=data.serial_number,
            batch_id=data.batch_id,
            name=data.name,
            dosage=data.dosage,
            description=data.description,
            qr_code=data.qr_code,

            created_at=datetime.now(),
            update_at=datetime.now()
        )

        self.drug_repository.create_drug(drug_to_create)

        # Build response
        return DrugResponse(
            id=drug_to_create.id,
            serial_number=drug_to_create.serial_number,
            batch_id=drug_to_create.batch_id,
            name=drug_to_create.name,
            dosage=drug_to_create.dosage,
            description=drug_to_create.description,
            qr_code=drug_to_create.qr_code,
            created_at=drug_to_create.created_at,
            updated_at=drug_to_create.updated_at
        )

    async def update_drug(self, data: DrugUpdate, current_user: User) -> DrugResponse:
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        drug_exists = self.drug_repository.get_drug_by_name(data.name)
        if drug_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this name already exists.")


        return DrugResponse()


