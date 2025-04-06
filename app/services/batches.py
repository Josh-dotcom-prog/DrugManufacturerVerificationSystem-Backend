from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


from app.models.batches import Batch, BatchStatus
from app.repository.batches import BatchesRepository
from app.schemas.batches import *
from app.responses.batches import *

from app.models.users import User, UserRole

from app.repository.manufacturer import ManufacturerRepository

from typing import List

class BatchService:
    def __int__(self, batch_repository: BatchesRepository, manufacturer_repository: ManufacturerRepository):
        self.batch_repository = batch_repository
        self.manufacturer_repository = manufacturer_repository

    async def create_batch(self, data: BatchCreate, current_user: User) -> BatchResponse:
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")

        # check if user is a manufacturer
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a manufacture to access this route.")

        # check if batch already exists
        batch_exists = self.batch_repository.get_batch_by_batch_number(data.batch_number)
        if batch_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Batch  with this name already exists.")

        # create the batch

        batch_to_create = Batch(
            batch_number=data.batch_number,
            manufacturer_id=data.manufacturer_id,
            maufacturing_date=data.manufacturing_date,
            batch_status=data.status.active.value,
            expiry_date=data.expiry_date,

            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.batch_repository.create_batches(batch_to_create)

        # return batch response
        return BatchResponse(
            id=batch_to_create.id,
            batch_number=batch_to_create.batch_number,
            manufacturer_id=batch_to_create.manufacturer_id,
            manufacturing_date=batch_to_create.manufacturing_date,
            status=batch_to_create.status,
            expiry_date=batch_to_create.expiry_date,
            created_at=batch_to_create.created_at,
            updated_at=batch_to_create.updated_at
        )

    async def update_batch(self, data: BatchUpdate, current_user: User) -> BatchResponse:
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")

        # check if user is a manufacturer
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if batch already exists
        batch_to_update = self.batch_repository.get_batch_by_batch_number(data.batch_number)
        if not batch_to_update:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Batch  with this name does not exists.")

        # Validate the batch_to_update data

        if data.manufacturing_date is not None:
            batch_to_update.manufacturing_date = data.manufacturing_date
        if data.expiry_date is not None:
            batch_to_update.expiry_date = data.expiry_date
        if data.status is not None:
            batch_to_update.status = data.status

        # update the batch
        self.batch_repository.update_batches(batch_to_update)

        return BatchResponse(
            id=batch_to_update.id,
            batch_number=batch_to_update.batch_number,
            manufacturer_id=batch_to_update.manufacturer_id,
            manufacturing_date=batch_to_update.manufacturing_date,
            status=batch_to_update.status,
            expiry_date=batch_to_update.expiry_date,
            created_at=batch_to_update.created_at,
            updated_at=batch_to_update.updated_at
        )

    async def delete_batch(self, batch_id: int,current_user: User):
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")

        # check if user is a manufacturer
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # check if batch already exists
        batch_to_delete = self.batch_repository.get_batch_by_batch_id(batch_id)
        if not batch_to_delete:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Batch  with this id does not exists.")

        # get manufacturer by this user_id
        manufacture = self.manufacturer_repository.get_manufacturer_by_user_id(current_user.id)
        if not manufacture:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route")

        # check if batch was created by the user
        if manufacture.id != batch_to_delete.manufacturer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User not authorized to delete this batch, probably created by another user.")

        # Proceed to delete the batch
        self.batch_repository.delete_batch(batch_to_delete)

        return JSONResponse("Batch deleted successfully.")


    async def get_batch_by_id(self, batch_id: int, current_user: User) -> BatchResponse:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")

        # check if user is a manufacturer
        if not current_user.role.value == UserRole.MANUFACTURER.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route.")

        # Revive the batch if it exists
        batch = self.batch_repository.get_batch_by_batch_id(batch_id)
        if not batch:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Batch  with this id does not exists.")

        # get manufacturer by this user_id
        manufacture = self.manufacturer_repository.get_manufacturer_by_user_id(current_user.id)
        if not manufacture:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not a manufacture to access this route")

        # check if batch was created by the user
        if manufacture.id != batch.manufacturer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User not authorized to access this batch, probably created by another user.")

        return BatchResponse(
            id=batch.id,
            batch_number=batch.batch_number,
            manufacturer_id=batch.manufacturer_id,
            manufacturing_date=batch.manufacturing_date,
            status=batch.status,
            expiry_date=batch.expiry_date,
            created_at=batch.created_at,
            updated_at=batch.updated_at
        )

    async def get_all_batches(self, current_user: User) -> List[BatchResponse]:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User is not active therefore can not be a manufacturer.")

        # check if user is a manufacturer
        if not current_user.role.value == UserRole.ADMIN.value:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not an admin to access this route.")

        # Revive the batch if it exists
        batches = self.batch_repository.get_all_batches()
        if not batches:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Batches not found.")



        return [BatchResponse(
            id=batch.id,
            batch_number=batch.batch_number,
            manufacturer_id=batch.manufacturer_id,
            manufacturing_date=batch.manufacturing_date,
            status=batch.status,
            expiry_date=batch.expiry_date,
            created_at=batch.created_at,
            updated_at=batch.updated_at
        )for batch in batches]


