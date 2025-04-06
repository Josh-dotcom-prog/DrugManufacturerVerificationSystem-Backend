from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.manufacturer import Manufacturer

class ManufacturerRepository:
    def __init__(self, session: Session):
        self.session = session

    #Creating manufacturer
    def create_manufacturer(self, manufacturer: Manufacturer):
        try:
            self.session.add(manufacturer)
            self.session.commit()
            self.session.refresh(manufacturer)
        except IntegrityError:
            self.session.rollback()
            raise

    #updating manufacturer
    def update_manufacturer(self, manufacturer: Manufacturer):
        try:
            self.session.merge(manufacturer)
            self.session.commit()
            self.session.refresh(manufacturer)
        except IntegrityError:
            self.session.rollback()
            raise

    #deleting manufacturer
    def delete_manufacturer(self, manufacturer: Manufacturer):
        self.session.delete(manufacturer)
        self.session.commit()


    #gets manufacturer by id
    def get_manufacturer_by_manufacturer_id(self, manufacturer_id: int) -> Manufacturer:
        return self.session.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()

    #lists all manufacturers
    def get_all_manufacturers(self):
        return self.session.query(Manufacturer).all()

    # get manufacturer by license_number
    def get_manufacturer_by_license_number(self, license_number: str) -> Manufacturer:
        return self.session.query(Manufacturer).filter(Manufacturer.license_number == license_number).first()

    def get_manufacturer_by_user_id(self, user_id: int) -> Manufacturer:
        return self.session.query(Manufacturer).filter(Manufacturer.user_id == user_id).first()
