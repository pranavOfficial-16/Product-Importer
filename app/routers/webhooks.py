import httpx
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.webhook import Webhook

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


# List webhooks
@router.get("/")
def list_webhooks(db: Session = Depends(get_db)):
    return db.query(Webhook).all()


# Create webhook
@router.post("/")
def create_webhook(data: dict, db: Session = Depends(get_db)):
    webhook = Webhook(url=data["url"], event=data["event"], enabled=True)
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


# Delete webhook
@router.delete("/{webhook_id}")
def delete_webhook(webhook_id: int, db: Session = Depends(get_db)):
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        return {"error": "Webhook not found"}

    db.delete(webhook)
    db.commit()
    return {"message": "Deleted"}


# Enable/Disable toggle
@router.put("/{webhook_id}/toggle")
def toggle_webhook(webhook_id: int, db: Session = Depends(get_db)):
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
    if not webhook:
        return {"error": "Webhook not found"}

    webhook.enabled = not webhook.enabled
    db.commit()
    db.refresh(webhook)
    return webhook


# Test webhook - send POST request
@router.post("/{webhook_id}/test")
def test_webhook(webhook_id: int, db: Session = Depends(get_db)):
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()

    if not webhook:
        return {"error": "Webhook not found"}

    if not webhook.enabled:
        return {"error": "Webhook disabled"}

    test_payload = {"message": "Webhook test successful", "event": webhook.event}

    start = time.time()
    try:
        with httpx.Client() as client:
            response = client.post(webhook.url, json=test_payload)
        elapsed = round((time.time() - start) * 1000)  # in ms
        return {"status_code": response.status_code, "response_time_ms": elapsed}
    except Exception as e:
        return {"error": str(e)}
