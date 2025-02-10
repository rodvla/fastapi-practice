from sqlmodel import Session, select
from app.models.patient import Patient

async def read_patients(session: Session
)-> list[Patient]:
    patients = session.exec(select(Patient)).all()
    return patients

async def save_patient(
    session: Session, name: str, email: str, phone: str, document_path: str
) -> None:
    new_patient = Patient(
        name=name, email=email, phone=phone, document_path=document_path
    )
    session.add(new_patient)
    session.commit()
    session.refresh(new_patient)
