from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.drugs import Drug

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
    def get_batch_by_drug_id(self, drug_id: int) -> Drug:
        return self.session.query(Drug).filter(Drug.id == drug_id).first()

    def get_drug_by_name(self, drug_name: str) -> Drug:
        return self.session.query(Drug).filter(Drug.name == drug_name).first()

    #lists all drugs
    def get_all_drugs(self):
        return self.session.query(Drug).all()

