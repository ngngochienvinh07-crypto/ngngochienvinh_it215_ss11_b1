from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import service
from database import Base, engine, get_db
from schemas import APIResponse, ParkingSlotCreate, ParkingSlotResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


def build_response(status_code: int, message: str, path: str, data=None, error=None) -> dict:
    """Helper dựng response chuẩn 6 trường: statusCode, message, error, data, path, timestamp."""
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat(),
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=build_response(
            status_code=exc.status_code,
            message="Request failed",
            path=str(request.url.path),
            error=exc.detail,
        ),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=build_response(
            status_code=500,
            message="Internal server error",
            path=str(request.url.path),
            error=str(exc),
        ),
    )


# ---- Endpoints ----

@app.post("/parking-slots", response_model=APIResponse, status_code=201)
def create_slot(request: Request, slot: ParkingSlotCreate, db: Session = Depends(get_db)):
    new_slot = service.create_parking_slot(db, slot)
    return build_response(
        status_code=201,
        message="Tạo parking slot thành công",
        path=str(request.url.path),
        data=ParkingSlotResponse.model_validate(new_slot).model_dump(),
    )


@app.get("/parking-slots", response_model=APIResponse)
def read_slots(request: Request, db: Session = Depends(get_db)):
    slots = service.get_all_parking_slots(db)
    data = [ParkingSlotResponse.model_validate(s).model_dump() for s in slots]
    return build_response(
        status_code=200,
        message="Lấy danh sách parking slot thành công",
        path=str(request.url.path),
        data=data,
    )


@app.get("/parking-slots/{slot_id}", response_model=APIResponse)
def read_slot(request: Request, slot_id: int, db: Session = Depends(get_db)):
    slot = service.get_parking_slot_by_id(db, slot_id)
    return build_response(
        status_code=200,
        message="Lấy chi tiết parking slot thành công",
        path=str(request.url.path),
        data=ParkingSlotResponse.model_validate(slot).model_dump(),
    )
