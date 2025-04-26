"""Generate demo patients + observations"""
from faker import Faker
from random import choice, uniform
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Patient, Observation, Gender

fake = Faker()
LOINCS = ["789-8", "718-7", "4544-3", "798-8"]
START_TS = datetime(2024, 1, 1, 8)

def seed(num_patients: int = 10):
    db: Session = SessionLocal()

    patients = []
    for i in range(num_patients):
        p = Patient(
            name=fake.name(),
            gender=Gender.male if i < num_patients/2 else Gender.female,
            birth_date=fake.date_between(start_date="-90y", end_date="-20y")
        )
        db.add(p)
        patients.append(p)
    db.commit()

    for p in patients:
        ts = START_TS
        for _ in range(20):
            loinc = choice(LOINCS)
            val = round(uniform(5.0, 15.0), 2)
            db.add(Observation(
                patient_id=p.id,
                loinc_num=loinc,
                value=val,
                valid_period=f"[{ts.isoformat()},{ts.isoformat()}]",
            ))
            ts += timedelta(hours=6)
    db.commit()
    db.close()
    print("Seeded ✔")

if __name__ == "__main__":
    seed()