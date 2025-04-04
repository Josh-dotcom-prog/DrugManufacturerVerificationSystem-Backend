from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.verificationHistory import Verification

class BatchesRepository:
    def __init__(self, session: Session):
        self.session = session

    #Creating a verificationHistory
    def create_history(self, verification: Verification):
        try:
            self.session.add(verification)
            self.session.commit()
            self.session.refresh(verification)
        except IntegrityError:
            self.session.rollback()
            raise

    #updating a verificationHistory
    def update_history(self, verification: Verification):
        try:
            self.session.merge(verification)
            self.session.commit()
            self.session.refresh(verification)
        except IntegrityError:
            self.session.rollback()
            raise

    #deleting a verification History
    def delete_history(self, verification: Verification):
        self.session.delete(verification)
        self.session.commit()


    #gets verification history by id
    def get_verification_by_drug_id(self, drug_id: int) -> Verification:
        return self.session.query(Verification).filter(Verification.id == drug_id).first()

    #lists all verification history
    def get_all_verification_history(self, drug_id: int):
        return self.session.query(Verification).all(Verification.id == drug_id).all()

