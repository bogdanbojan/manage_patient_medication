from . import db
import enum

class GenderEnum(enum.Enum):
    """Enum data type for patients' gender."""

    male = "male"
    female = "female"
    unknown = "unknown"

class Patient(db.Model):
    """Data model for patients."""

    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(160))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    gender = db.Column(db.Enum(GenderEnum))
    date_of_birth = db.Column(db.Date)
    modify_date = db.Column(db.Date)

    medications = db.relationship("Medication", backref='patient')



    def __repr__(self):
        return f"{self.first_name} - {self.description}"

class UnitEnum(enum.Enum):
    """Emum data type for medications' unit."""

    kg = "kg"
    g = "g"
    mg = "mg"
    mcg = "mcg"
    l = "l"
    ml = "ml"
    cc = "cc"
    mol = "mol"
    mmol = "mmol"


class Medication(db.Model):
    """Data model for medications."""

    medication_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(160))
    dosage = db.Column(db.Integer)
    unit = db.Column(db.Enum(UnitEnum))
    time = db.Column(db.Time)
    creation_date = db.Column(db.Date)
    modify_date = db.Column(db.Date)

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
