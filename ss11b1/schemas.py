from pydantic import BaseModel

class CreateParkingSlot(BaseModel):
    slot_code: str
    zone_name: str
    max_weight: int
    is_available: bool = True
