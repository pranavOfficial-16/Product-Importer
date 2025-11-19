import redis
from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/progress", tags=["Progress"])

redis_client = redis.Redis.from_url(settings.REDIS_URL)


@router.get("/{job_id}")
def get_progress(job_id: str):
    data = redis_client.hgetall(f"job:{job_id}")

    if not data:
        return {"status": "not_found"}

    response = {k.decode(): v.decode() for k, v in data.items()}
    return response
