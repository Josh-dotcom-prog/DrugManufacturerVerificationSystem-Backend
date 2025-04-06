from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.models.manufacturer import Manufacturer
from app.repository.manufacturer import ManufacturerRepository
from app.schemas.manufacturer import *
from app.responses.manufacturer import *

from app.models.users import User

from datetime import datetime


class ManufacturerService:
    def __init__(self, manufacturer_repository: ManufacturerRepository):
        self.manufacturer_repository = manufacturer_repository

    async def create_manufacturer(self, current_user:User, data: ManufacturerCreate) -> ManufacturerResponse:

        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active therefore can not be a manufacturer." )

        # check if manufacturer already exists
        manufacturer_exists = self.manufacturer_repository.get_manufacturer_by_license_number(data.license_number)

        if manufacturer_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer with this license number already exists.")

        # proceed to create manufacturer

        manufacture = Manufacturer(
            name=data.name,
            license_number=data.license_number,
            address=data.address,
            contact_email=data.contact_email,
            contact_phone=data.contact_phone,
            user_id=current_user.id,
            license_file=data.license_file,
            certificate_file=data.certificate_file,

            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Proceed to create the manufacture to the database

        self.manufacturer_repository.create_manufacturer(manufacture)

        # build a manufacture response model

        manufacture_response = ManufacturerResponse(
            id=manufacture.id,
            name=manufacture.name,
            license_number=manufacture.license_number,
            address=manufacture.address,
            contact_email=manufacture.contact_email,
            contact_phone=manufacture.contact_phone,
            license_file=manufacture.license_file,
            certificate_file=manufacture.certificate_file,

            created_at=manufacture.created_at,
            updated_at=manufacture.updated_at
        )

        return manufacture_response

    async def update_manufacturer(self, current_user: User, data: ManufacturerUpdate) -> ManufacturerResponse:
        # check if user is verified
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active therefore can not be a manufacturer." )

        # check if manufacturer already exists
        manufacturer_to_update = self.manufacturer_repository.get_manufacturer_by_user_id(current_user.id)
        if not manufacturer_to_update:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manufacturer with this id does not  exists.")

        # proceed to update manufacturer

        if data.name is not None:
            manufacturer_to_update.name = data.name
        if data.address is not None:
            manufacturer_to_update.address = data.address
        if data.license_file is not None:
            manufacturer_to_update.license_file = data.license_file
        if data.certificate_file is not None:
            manufacturer_to_update.certificate_file = data.certificate_file
        if data.contact_email is not None:
            manufacturer_to_update.contact_email = data.contact_email
        if data.contact_phone is not None:
            manufacturer_to_update.contact_phone = data.contact_phone
        if data.license_number is not None:
            manufacturer_to_update.license_number = data.license_number

        self.manufacturer_repository.update_manufacturer(manufacturer_to_update)

        return ManufacturerResponse(
            id=manufacturer_to_update.id,
            name=manufacturer_to_update.name,
            license_number=manufacturer_to_update.license_number,
            address=manufacturer_to_update.address,
            contact_email=manufacturer_to_update.contact_email,
            contact_phone=manufacturer_to_update.contact_phone,
            license_file=manufacturer_to_update.license_file,
            certificate_file=manufacturer_to_update.certificate_file,

            created_at=manufacturer_to_update.created_at,
            updated_at=manufacturer_to_update.updated_at
        )

