from sqlmodel import SQLModel, Field


class Patient(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str
    phone: str
    document_path: str
