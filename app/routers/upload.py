import uuid
import os
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from app.config import settings
from app.workers.tasks import import_csv_task

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    # Validate CSV
    if not file.filename.endswith(".csv"):
        return JSONResponse({"error": "Only CSV files allowed"}, status_code=400)

    # Generate job ID
    job_id = str(uuid.uuid4())

    # Save file temporarily
    save_path = os.path.join(settings.UPLOAD_DIR, f"{job_id}.csv")

    with open(save_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    # Run Celery task
    import_csv_task.delay(job_id, save_path)

    return {"job_id": job_id, "message": "Upload started"}
