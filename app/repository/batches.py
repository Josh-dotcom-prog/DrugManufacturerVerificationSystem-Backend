from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.batches import Batch

class BatchesRepository:
    def __init__(self, session: Session):
        self.session = session

    #Creating batch
    def create_batches(self, batches: Batch):
        try:
            self.session.add(batches)
            self.session.commit()
            self.session.refresh(batches)
        except IntegrityError:
            self.session.rollback()
            raise

    #updating batches
    def update_batches(self, batches: Batch):
        try:
            self.session.merge(batches)
            self.session.commit()
            self.session.refresh(batches)
        except IntegrityError:
            self.session.rollback()
            raise

    #deleting batches
    def delete_manufacturer(self, batches: Batch):
        self.session.delete(batches)
        self.session.commit()


    #gets batches by id
    def get_batch_by_batch_id(self, batch_id: int) -> Batch:
        return self.session.query(Batch).filter(Batch.id == batch_id).first()

    #lists all batches
    def get_all_batches(self):
        return self.session.query(Batch).all()

