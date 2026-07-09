from sqlalchemy.orm import Session
from models import ParkingSlotModel
from schemas import CreateParkingSlot

def get_all_parking_slots_service(db: Session):
    list_slots = db.query(ParkingSlotModel).all()
    return list_slots

def get_parking_slot_by_id_service(id: int, db: Session):
    slot_in_db = db.query(ParkingSlotModel).filter(ParkingSlotModel.id == id).first()
    return slot_in_db

def create_parking_slot_service(new_slot: CreateParkingSlot, db: Session):
    slot = ParkingSlotModel(**new_slot.model_dump())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot
