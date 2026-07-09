from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
Base = declarative_base()

class ParkingSlotModel(Base):
    __tablename__ = "parking_slots"
    id = Column(Integer, autoincrement=True, primary_key=True)
    slot_code = Column(String(50), nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
