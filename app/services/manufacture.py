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