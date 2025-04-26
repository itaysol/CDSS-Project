"""Create tables + PL/pgSQL trigger (run once)"""
from sqlalchemy import text
from app.database import engine
from app import models

models.Base.metadata.create_all(engine)

SQL = """
CREATE OR REPLACE FUNCTION close_current_version()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.txn_end IS NULL THEN
     UPDATE observations
       SET txn_end = NOW()
       WHERE patient_id = NEW.patient_id
         AND loinc_num  = NEW.loinc_num
         AND lower(valid_period) = lower(NEW.valid_period)
         AND txn_end IS NULL;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_obs_version ON observations;
CREATE TRIGGER trg_obs_version
BEFORE INSERT OR UPDATE ON observations
FOR EACH ROW EXECUTE FUNCTION close_current_version();
"""
with engine.begin() as conn:
    conn.execute(text(SQL))
print("Schema & triggers created ✔")