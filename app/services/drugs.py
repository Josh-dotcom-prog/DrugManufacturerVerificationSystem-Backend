from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.drugs import Drug
from app.repository.drugs import DrugRepository
from app.schemas.drugs import *
from app.responses.drugs import *

from app.models.users import User, UserRoleEnum, ApprovalStatus
from app.repository.users import UserRepository

from datetime import datetime

from typing import List


class DrugService:
    def __init__(self, drug_repository: DrugRepository, user_repository: UserRepository):
        self.drug_repository = drug_repository
        self.user_repository = user_repository

    async  def create_drug(self, data: DrugCreate, current_user: User) -> DrugResponse:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not access this route")
        # check user role
        if not current_user.role.value == UserRoleEnum.manufacturer.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a manufacture to access this route.")

        # check if manufacture is approved
        if not current_user.approval_status == ApprovalStatus.approved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer is not approved yet.")

        # check if drug with this name exists
        drug_exists = self.drug_repository.get_drug_by_name(data.name)
        if drug_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this name already exists.")

        # check if batch with this id exists
        batch_number = self.drug_repository.get_drug_by_batch_number(data.batch_number)
        if batch_number:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this batch already exists.")

        # get manufacturer with this user id
        manufacturer = self.user_repository.get_user_by_id(current_user.id)
        if not manufacturer:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer with this user id does not exists")


        # Proceed to create the drug
        # Create new drug
        drug = Drug(
            name=data.name,
            category=data.category,
            dosage_form=data.dosage_form,
            batch_number=data.batch_number,
            country_of_origin=data.country_of_origin,
            manufacturing_date=data.manufacturing_date,
            expiry_date=data.expiry_date,
            description=data.description,
            manufacturer_id=current_user.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.drug_repository.create_drug(drug)

        return DrugResponse(
            id=drug.id,
            name=drug.name,
            category=drug.category,
            dosage_form=drug.dosage_form,
            batch_number=drug.batch_number,
            country_of_origin=drug.country_of_origin,
            manufacturer=manufacturer.name,
            manufacturing_date=drug.manufacturing_date,
            expiry_date=drug.expiry_date,
            description=drug.description,
            created_at=drug.created_at,
            updated_at=drug.updated_at,
        )

    async def update_drug(self, data: DrugUpdate, current_user: User) -> DrugResponse:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        # check user role
        if not current_user.role.value == UserRoleEnum.manufacturer.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if manufacture is approved
        if not current_user.approval_status == ApprovalStatus.approved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer is not approved yet.")

        # check if drug with this name exists
        drug_to_update = self.drug_repository.get_drug_by_name(data.name)
        if not drug_to_update:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Drug with this name does not exists.")

        # check if drug was created by this manufacturer
        if not current_user.id == drug_to_update.manufacturer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Can not update drug you didn't create.")

        # validate update data
        if data.name is not None:
            drug_to_update.name = data.name
        if data.dosage_form is not None:
            drug_to_update.dosage_form = data.dosage_form
        if data.description is not None:
            drug_to_update.description = data.description

        # proceed to update the drug
        updated_drug = self.drug_repository.update_drug(drug_to_update)

        # check manufacturer
        manufacturer = self.user_repository.get_user_by_id(updated_drug.manufacturer_id)
        if not manufacturer:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer with this user_id not found")


        # Build and return response
        return DrugResponse(
            id=updated_drug.id,
            name=updated_drug.name,
            category=updated_drug.category,
            dosage_form=updated_drug.dosage_form,
            batch_number=updated_drug.batch_number,
            country_of_origin=updated_drug.country_of_origin,
            manufacturer=manufacturer.name,
            manufacturing_date=updated_drug.manufacturing_date,
            expiry_date=updated_drug.expiry_date,
            description=updated_drug.description,
            created_at=updated_drug.created_at,
            updated_at=updated_drug.updated_at,
        )

    async def delete_drug(self, drug_id: int, current_user: User):
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        # check user role
        if not current_user.role.value == UserRoleEnum.manufacturer.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if manufacture is approved
        if not current_user.approval_status == ApprovalStatus.approved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer is not approved yet.")


        # check if drug with this name exists
        drug_to_delete = self.drug_repository.get_drug_by_drug_id(drug_id)
        if not drug_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug with this id not found.")

        # Get all drug ids created by this manufacturer
        drugs = self.drug_repository.get_all_drugs_by_one_manufacturer(current_user.id)
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
        if not current_user.role.value == UserRoleEnum.manufacturer.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if manufacture is approved
        if not current_user.approval_status == ApprovalStatus.approved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer is not approved yet.")


        # Get all drug ids created by this manufacturer
        drugs = self.drug_repository.get_all_drugs_by_one_manufacturer(current_user.id)
        if not drugs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Manufacturer does not have any drugs")
        return [DrugResponse(
            id=drug.id,
            name=drug.name,
            category=drug.category,
            dosage_form=drug.dosage_form,
            batch_number=drug.batch_number,
            country_of_origin=drug.country_of_origin,
            manufacturer=drug.manufacturer.name,
            manufacturing_date=drug.manufacturing_date,
            expiry_date=drug.expiry_date,
            description=drug.description,
            created_at=drug.created_at,
            updated_at=drug.updated_at,
        )for drug in drugs]

    async def get_drug_detail(self, drug_id: int, current_user:User) -> DrugResponse:
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")
        # check user role
        if not current_user.role.value == UserRoleEnum.manufacturer.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if manufacture is approved
        if not current_user.approval_status == ApprovalStatus.approved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer is not approved yet.")

        # Get all drug ids created by this manufacturer
        drug = self.drug_repository.get_drug_by_drug_id(drug_id)
        if not drug:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Drug with this id does not exists.")
        return DrugResponse(
            id=drug.id,
            name=drug.name,
            category=drug.category,
            dosage_form=drug.dosage_form,
            batch_number=drug.batch_number,
            country_of_origin=drug.country_of_origin,
            manufacturer=drug.manufacturer.name,
            manufacturing_date=drug.manufacturing_date,
            expiry_date=drug.expiry_date,
            description=drug.description,
            created_at=drug.created_at,
            updated_at=drug.updated_at,
        )


    async def get_drug_dashboard(self, current_user: User) -> DrugDashboard:
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")

        # check user role
        if not current_user.role.value == UserRoleEnum.manufacturer.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if manufacture is approved
        if not current_user.approval_status == ApprovalStatus.approved:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer is not approved yet.")

        expired_drugs = self.drug_repository.get_expired_drugs_by_manufacturer(current_user.id)

        # active drugs
        active_drugs = self.drug_repository.get_active_drugs_by_manufacturer(current_user.id)

        if not expired_drugs and active_drugs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You don't have any drugs in the system")

        # build expired drugs response
        expired_drugs_response = [ExpiredDrugs(
            drug_name=expired_drug.name,
            status=DrugStatus.expired
        ) for expired_drug in expired_drugs]

        # build active drugs response
        active_drugs_response = [ActiveDrugs(
            drug_name=active_drug.name,
            status=DrugStatus.active
        )for active_drug in active_drugs]

        # Count stats
        active_count = len(active_drugs)
        expired_count = len(expired_drugs)
        total = active_count + expired_count

        return DrugDashboard(
            active=active_drugs_response,
            expired=expired_drugs_response,
            active_count=active_count,
            expired_count=expired_count,
            total=total
        )