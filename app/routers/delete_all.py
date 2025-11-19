import uuid
from fastapi import APIRouter
from app.workers.tasks import delete_all_products_task

router = APIRouter(prefix="/products", tags=["Products"])


@router.delete("/delete-all")
def delete_all_products():
    # Create a job ID for progress tracking
    job_id = str(uuid.uuid4())

    # Trigger Celery task
    delete_all_products_task.delay(job_id)

    return {"job_id": job_id, "message": "Delete started"}
