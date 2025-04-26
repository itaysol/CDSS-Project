from datetime import datetime, date as dtdate
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from app import models

# HISTORY

def get_history(db: Session, patient_id: int, loinc_num: str, start: datetime, end: datetime):
    q = (
        select(models.Observation.value,
               func.lower(models.Observation.valid_period).label("taken_at"),
               models.LoincConcept.long_name)
        .join(models.LoincConcept)
        .where(models.Observation.patient_id == patient_id,
               models.Observation.loinc_num == loinc_num,
               models.Observation.valid_period.op("&&")(func.tstzrange(start, end, '[]')),
               models.Observation.txn_end.is_(None))
        .order_by("taken_at")
    )
    return db.execute(q).all()

# UPDATE

def update_observation(db: Session, patient_id: int, loinc_num: str, taken_at: datetime, new_value: float):
    current = db.execute(
        select(models.Observation).where(
            models.Observation.patient_id == patient_id,
            models.Observation.loinc_num == loinc_num,
            func.lower(models.Observation.valid_period) == taken_at,
            models.Observation.txn_end.is_(None))
    ).scalar_one_or_none()

    if current:
        db.execute(update(models.Observation)
                   .where(models.Observation.id == current.id)
                   .values(txn_end=func.now()))

    new_obs = models.Observation(
        patient_id=patient_id,
        loinc_num=loinc_num,
        value=new_value,
        valid_period=func.tstzrange(taken_at, taken_at, '[]'),
    )
    db.add(new_obs)
    db.commit()
    db.refresh(new_obs)
    return new_obs

# DELETE

def delete_latest(db: Session, patient_id: int, loinc_num: str, date_: dtdate):
    sub = (
        select(models.Observation.id)
        .where(models.Observation.patient_id == patient_id,
               models.Observation.loinc_num == loinc_num,
               func.date(func.lower(models.Observation.valid_period)) == date_,
               models.Observation.txn_end.is_(None))
        .order_by(func.lower(models.Observation.valid_period).desc())
        .limit(1)
    )
    obs_id = db.scalar(sub)
    if not obs_id:
        return False
    db.execute(update


---
## 1️⃣ app/api.py
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import HistoryRequest, UpdateRequest, DeleteRequest, ObservationOut
from app import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/history", response_model=list[ObservationOut])
async def history(req: HistoryRequest, db: Session = Depends(get_db)):
    rows = crud.get_history(db, **req.dict())
    return [{"takenAt": r.taken_at, "value": r.value, "loincLongName": r.long_name} for r in rows]

@router.post("/update")
async def update(req: UpdateRequest, db: Session = Depends(get_db)):
    obs = crud.update_observation(db, **req.dict())
    return {"id": obs.id, "newValue": obs.value}

@router.post("/delete")
async def delete(req: DeleteRequest, db: Session = Depends(get_db)):
    ok = crud.delete_latest(db, **req.dict())
    if not ok:
        raise HTTPException(status_code=404, detail="Measurement not found for given date")
    return {"status": "deleted"}