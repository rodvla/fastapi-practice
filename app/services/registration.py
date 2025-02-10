from fastapi import BackgroundTasks, UploadFile
from pydantic import EmailStr
from sqlmodel import Session

from app.services.email import send_email
from app.services.file import save_file
from app.repository.repository import save_patient


async def register_patient(
    session: Session,
    background_tasks: BackgroundTasks,
    name: str,
    email_address: EmailStr,
    phone: str,
    document: UploadFile,
) -> None:
    document_path = await save_file(document)
    await save_patient(session, name, email_address, phone, document_path)
    await send_email(background_tasks, email_address)
