# models.py
# Pydantic BaseModel = a class with built-in type validation
# Every field is type-annotated - Python knows WHAT data to expect
# If wrong data type is passed, Pydantic raises an error immediately

from pydantic import BaseModel, field_validator
from typing import Optional

class UserProfile(BaseModel):
    # --- MODULE 1: Personal Identity ---
    full_name: str
    date_of_birth: str
    nationality: str
    city: str
    email: str
    phone: str
    address: Optional[str] = None

    # --- MODULE 2: Academic Background ---
    university: str
    degree: str                             #e.g. M.Sc. Bauingenieurwesen
    thesis_title: Optional[str] = None      # None = Not required
    grade: Optional[str] = None             # German scale: 1.0 (best) → 4.0

    # --- MODULE 3: AEC Experience ---
    bim_roles: list[str] = []               # ["BIM Modeler", "BIM Koordinator"]
    software_skills: list[str] = []         # ["Revit", "IfcOpenShell", "Python"]
    years_experience: int = 0

    # --- MODULE 4: Target Job ---
    target_job_title: str
    target_company: str
    job_reference_number: Optional[str] = None
    job_ad_text: str                        # raw paste of the job advertisement

    # --- MODULE 5: Parsed from uploaded documents ---
    cv_extracted_text: Optional[str] = None
    cover_letter_extracted_text: Optional[str] = None

    # VALIDATOR: German grades are 1.0-4.0, not percentages or GPA
    @field_validator("grade")
    @classmethod
    def validate_german_grade(cls, v):
        if v is not None and not (1.0 <= v <= 4.0):
            raise ValueError("Note muss zwischen 1.0 und 4.0 liegen")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v is None or "@" not in v or "." not in v:
            raise ValueError("E-Mail-Adresse ist ungültig — '@' und '.' werden benötigt")
        return v




