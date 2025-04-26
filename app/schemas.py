from datetime import datetime, date
from pydantic import BaseModel, Field

class HistoryRequest(BaseModel):
    patient_id: int
    loinc_num: str
    start: datetime
    end: datetime

class ObservationOut(BaseModel):
    taken_at: datetime = Field(alias="takenAt")
    value: float
    loinc_long_name: str = Field(alias="loincLongName")

class UpdateRequest(BaseModel):
    patient_id: int
    loinc_num: str
    taken_at: datetime
    new_value: float

class DeleteRequest(BaseModel):
    patient_id: int
    loinc_num: str
    date: date