from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import shutil
import os
from tasks import process_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

job_status = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    job_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    job_status[job_id] = "Processing"
    process_file.delay(job_id, file_path)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    status = job_status.get(job_id, "Not found")
    output_file = os.path.join(OUTPUT_DIR, f"{job_id}.txt")
    if status == "Done" and os.path.exists(output_file):
        with open(output_file, "r") as f:
            content = f.read()
        return {"job_id": job_id, "status": status, "output": content}
    return {"job_id": job_id, "status": status}
