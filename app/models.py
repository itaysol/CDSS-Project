import enum
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Float, TIMESTAMP, Index
from sqlalchemy.dialects.postgresql import TSTZRANGE
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Gender(str, enum.Enum):
    male = "M"
    female = "F"

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    birth_date = Column(Date)
    observations = relationship("Observation", back_populates="patient")

class LoincConcept(Base):
    __tablename__ = "concepts_loinc"
    loinc_num = Column(String, primary_key=True)
    long_name = Column(String, nullable=False)
    unit = Column(String)

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    loinc_num = Column(String, ForeignKey("concepts_loinc.loinc_num"), nullable=False)
    value = Column(Float, nullable=False)
    valid_period = Column(TSTZRANGE, nullable=False)
    txn_start = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    txn_end = Column(TIMESTAMP(timezone=True))

    patient = relationship("Patient", back_populates="observations")
    concept = relationship("LoincConcept")

    __table_args__ = (
        Index("ix_obs_patient_loinc_valid", "patient_id", "loinc_num", "valid_period", postgresql_using="gist"),
    )