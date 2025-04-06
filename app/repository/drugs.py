from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.drugs import Drug

from app.models.batches import Batch
from app.models.manufacturer import Manufacturer

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
        return  self.session.query(Drug).join(Batch, Drug.batch_id == Batch.id).filter(Batch.manufacturer_id == manufacturer_id).all()

    #lists all drugs
    def get_all_drugs(self):
        return self.session.query(Drug).all()

