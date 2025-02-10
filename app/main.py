from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, UploadFile, Form, File, BackgroundTasks, HTTPException
from pydantic import EmailStr
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.database.database import create_db_and_tables, SessionDep
from app.services.registration import register_patient
from app.repository.repository import read_patients


app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

@app.get("/patients/")
async def getPatients(
    session: SessionDep
) :
    patients= await read_patients(session)
    return {"patients" : patients}

@app.post("/register/", status_code=201)
async def register(
    session: SessionDep,
    background_tasks: BackgroundTasks,
    name: Annotated[str, Form(max_length=50)],
    email: Annotated[EmailStr, Form()],
    phone: Annotated[str, Form(pattern=r"^\+?[1-9]\d{1,14}$")],
    document: UploadFile = File(...),
) -> dict:
    try:
        await register_patient(session, background_tasks, name, email, phone, document)
        return {"message": "Patient registered successfully."}
    except Exception:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration. Please try again later.",
        )
