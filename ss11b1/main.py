from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from parking_slot_service import get_all_parking_slots_service, get_parking_slot_by_id_service, create_parking_slot_service
from schemas import CreateParkingSlot

app = FastAPI()

@app.get('/test-connction')
def test_connect(db: Session = Depends(get_db)):
    try:
        db.execute(text('SELECT 1'))
        return{
            "message": "SUCCESS"
        }
    except Exception as err:
        return{
            "message": str(err)
        }        

@app.get('/parking-slots')
def get_all_slots(db: Session = Depends(get_db)):
    list_slots = get_all_parking_slots_service(db)
    return {
        "message": "SUCESS",
        "data": list_slots
    }

@app.get('/parking-slots/{id}')
def get_slot_by_id(id: int, db: Session = Depends(get_db)):
    slot = get_parking_slot_by_id_service(id, db)
    if slot is None:
        raise HTTPException(status_code=404, detail="Parking slot khong ton tai")
    return{
        "message": "Success!",
        "data": slot
    }

@app.post('/parking-slot')
def create_slot(new_slot: CreateParkingSlot, db: Session = Depends(get_db)):
    slot = create_parking_slot_service(new_slot, db)
    return {
        "message": "Success!",
        "data": slot
    }
