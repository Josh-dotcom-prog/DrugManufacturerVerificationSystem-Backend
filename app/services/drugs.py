from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.drugs import Drug
from app.repository.drugs import DrugRepository
from app.schemas.drugs import *
from app.responses.drugs import *

from app.models.users import User, UserRole

from app.repository.batches import BatchesRepository
from app.repository.manufacturer import ManufacturerRepository

from datetime import datetime

from typing import List


class DrugService:
    def __init__(self, drug_repository: DrugRepository, batch_repository: BatchesRepository,
                 manufacturer_repository: ManufacturerRepository):
        self.drug_repository = drug_repository
        self.batch_repository = batch_repository
        self.manufacturer_repository = manufacturer_repository

    async  def create_drug(self, data: DrugCreate, current_user: User) -> DrugResponse:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        # check user role
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a manufacture to access this route.")

        # check if drug with this name exists
        drug_exists = self.drug_repository.get_drug_by_name(data.name)
        if drug_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this name already exists.")

        # check if batch with this id exists
        batch_exists = self.batch_repository.get_batch_by_batch_id(data.batch_id)
        if not batch_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Batch with this id does not exists.")


        # get manufacturer with this user id
        manufacturer = self.manufacturer_repository.get_manufacturer_by_user_id(current_user.id)
        if not manufacturer:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer with this user id does not exists")
        # check if batch was created by this manufacturer
        if not manufacturer.id == batch_exists.manufacturer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can not add drug to batch you didn't create")

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
        # check user role
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if drug with this name exists
        drug_to_update = self.drug_repository.get_drug_by_name(data.name)
        if not drug_to_update:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this name does not exists.")

        # check if batch with this id exists
        batch_exists = self.batch_repository.get_batch_by_batch_id(data.batch_id)
        if not batch_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Batch with this id does not exists.")

        # get manufacturer with this user id
        manufacturer = self.manufacturer_repository.get_manufacturer_by_user_id(current_user.id)
        if not manufacturer:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Manufacturer with this user id does not exists")
        # check if batch was created by this manufacturer
        if not manufacturer.id == batch_exists.manufacturer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Can not update drug to batch you didn't create")

        # Get all drug ids created by this manufacturer
        drugs = self.drug_repository.get_all_drugs_by_one_manufacturer(manufacturer.id)
        if not drugs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Manufacturer does not have any drugs")

        drugs_id = {drug.id for drug in drugs}

        # check if drug was created by this manufacturer
        if drug_to_update.id not in drugs_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not allowed to update a drug that doesn't belong to you")

        # validate update data
        if data.name is not None:
            drug_to_update.name = data.name
        if data.dosage is not None:
            drug_to_update.dosage = data.dosage
        if data.description is not None:
            drug_to_update.description = data.description
        if data.is_verified is not None:
            drug_to_update.is_verified = data.is_verified

        # proceed to update the drug
        self.drug_repository.update_drug(drug_to_update)

        # Build response
        return DrugResponse(
            id=drug_to_update.id,
            serial_number=drug_to_update.serial_number,
            batch_id=drug_to_update.batch_id,
            name=drug_to_update.name,
            dosage=drug_to_update.dosage,
            description=drug_to_update.description,
            qr_code=drug_to_update.qr_code,
            created_at=drug_to_update.created_at,
            updated_at=drug_to_update.updated_at
        )

    async def delete_drug(self, drug_id: int, current_user: User):
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        # check user role
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if drug with this name exists
        drug_to_delete = self.drug_repository.get_drug_by_drug_id(drug_id)
        if not drug_to_delete:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this name does not exists.")


        # get manufacturer with this user id
        manufacturer = self.manufacturer_repository.get_manufacturer_by_user_id(current_user.id)
        if not manufacturer:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Manufacturer with this user id does not exists")

        # Get all drug ids created by this manufacturer
        drugs = self.drug_repository.get_all_drugs_by_one_manufacturer(manufacturer.id)
        if not drugs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Manufacturer does not have any drugs")

        drugs_id = { drug.id for drug in drugs }

        # check if drug was created by this manufacturer
        if drug_to_delete.id not in drugs_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not allowed to delete a drug that doesn't belong to you")
        # delete the drug
        self.drug_repository.delete_drug(drug_to_delete)

        return JSONResponse("Drug with this id deleted successfully.")

    async def get_all_my_drugs(self, current_user: User) -> List[DrugResponse]:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        # check user role
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # get manufacturer with this user id
        manufacturer = self.manufacturer_repository.get_manufacturer_by_user_id(current_user.id)
        if not manufacturer:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Manufacturer with this user id does not exists")

        # Get all drug ids created by this manufacturer
        drugs = self.drug_repository.get_all_drugs_by_one_manufacturer(manufacturer.id)
        if not drugs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Manufacturer does not have any drugs")
        return [DrugResponse(
            id=drug.id,
            serial_number=drug.serial_number,
            batch_id=drug.batch_id,
            name=drug.name,
            dosage=drug.dosage,
            description=drug.description,
            qr_code=drug.qr_code,
            created_at=drug.created_at,
            updated_at=drug.updated_at
        ) for drug in drugs]