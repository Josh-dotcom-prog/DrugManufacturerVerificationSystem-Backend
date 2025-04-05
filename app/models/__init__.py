from .manufacturer import Manufacturer
from .batches import Batch
from .drugs import Drug

from sqlalchemy.orm import relationship


# Define relationships after all classes are fully defined
Manufacturer.batches = relationship("Batch", back_populates="manufacturer")
Batch.manufacturer = relationship("Manufacturer", back_populates="batches")

# Add the relationship between Batch and Drug
Batch.drugs = relationship("Drug", back_populates="batch")
Drug.batch = relationship("Batch", back_populates="drugs")

# verification
drug = relationship('Drug', back_populates='verifications')


# Drug
batch = relationship('Batch', back_populates='drugs')
verifications = relationship('Verification', back_populates='drug')
