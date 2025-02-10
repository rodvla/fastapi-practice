import os
import shutil

from fastapi import UploadFile

document_dir = "documents"


async def save_file(document: UploadFile) -> str:
    os.makedirs(document_dir, exist_ok=True)
    document_path = os.path.join(document_dir, document.filename)
    with open(document_path, "wb") as buffer:
        shutil.copyfileobj(document.file, buffer)
    return document_path
