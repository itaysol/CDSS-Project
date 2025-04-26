"""Load subset of LOINC concepts from CSV"""
import csv, pathlib
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import LoincConcept

CSV_PATH = pathlib.Path("data/loinc_subset.csv")

def load():
    db: Session = SessionLocal()
    with CSV_PATH.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            db.merge(LoincConcept(
                loinc_num=row["LOINC_NUM"],
                long_name=row["LONG_COMMON_NAME"],
                unit=row.get("EXAMPLE_UCUM_UNITS")
            ))
    db.commit()
    db.close()
    print("LOINC loaded ✔")

if __name__ == "__main__":
    load()