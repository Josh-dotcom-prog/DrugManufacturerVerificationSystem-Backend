from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.drugs import Drug
from datetime import datetime



class DrugRepository:
    def __init__(self, session: Session):
        self.session = session

    #Creating a drug
    def create_drug(self, drugs: Drug):
        try:
            self.session.add(drugs)
            self.session.commit()
            self.session.refresh(drugs)
        except IntegrityError:
            self.session.rollback()
            raise

    #updating a drug
    def update_drug(self, drugs: Drug):
        try:
            self.session.merge(drugs)
            self.session.commit()
            self.session.refresh(drugs)
            return drugs
        except IntegrityError:
            self.session.rollback()
            raise

    #deleting a drug
    def delete_drug(self, drugs: Drug):
        self.session.delete(drugs)
        self.session.commit()


    #gets batches by id
    def get_drug_by_drug_id(self, drug_id: int) -> Drug:
        return self.session.query(Drug).filter(Drug.id == drug_id).first()

    def get_drug_by_name(self, drug_name: str) -> Drug:
        return self.session.query(Drug).filter(Drug.name == drug_name).first()

    def get_all_drugs_by_one_manufacturer(self, manufacturer_id: int):
        return self.session.query(Drug).filter(Drug.manufacturer_id == manufacturer_id).all()

    def get_drug_by_batch_number(self, batch_number: str) -> Drug:
        return self.session.query(Drug).filter(Drug.batch_number == batch_number).first()

    def get_expired_drugs_by_manufacturer(self,  manufacturer_id: int):
        return (
            self.session.query(Drug)
            .filter(
                Drug.manufacturer_id == manufacturer_id,
                Drug.expiry_date < datetime.now()
            )
            .all()
        )

    def get_active_drugs_by_manufacturer(self, manufacturer_id: int):
        return (
            self.session.query(Drug)
            .filter(
                Drug.manufacturer_id == manufacturer_id,
                Drug.expiry_date > datetime.now()
            )
            .all()
        )