import os
import csv
import redis

from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.product import Product
from app.workers.celery_app import celery_app

# Redis client for progress tracking
redis_client = redis.Redis.from_url(settings.REDIS_URL)


def update_progress(job_id, progress, status):
    redis_client.hset(f"job:{job_id}", mapping={"progress": progress, "status": status})


@celery_app.task
def import_csv_task(job_id, file_path):
    update_progress(job_id, 0, "Starting...")

    db: Session = SessionLocal()

    try:
        # Count total rows for progress calculation
        with open(file_path, "r", encoding="utf-8") as f:
            total_rows = sum(1 for _ in f)

        update_progress(job_id, 5, "Parsing CSV")

        # Read again for actual import
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            processed = 0
            for row in reader:
                sku = row["sku"].lower()

                product = db.query(Product).filter(Product.sku == sku).first()

                if product:
                    # Update existing product
                    product.name = row["name"]
                    product.description = row["description"]
                    product.price = float(row["price"])
                else:
                    # Insert new product
                    new_product = Product(
                        sku=sku,
                        name=row["name"],
                        description=row["description"],
                        price=float(row["price"]),
                        active=True,
                    )
                    db.add(new_product)

                processed += 1
                if processed % 500 == 0:
                    db.commit()
                    progress = int((processed / total_rows) * 100)
                    update_progress(job_id, progress, "Importing...")

            db.commit()

        update_progress(job_id, 100, "Completed")
        return {"message": "Import completed"}

    except Exception as e:
        update_progress(job_id, -1, f"Failed: {str(e)}")
        return {"error": str(e)}

    finally:
        db.close()
        if os.path.exists(file_path):
            os.remove(file_path)


@celery_app.task
def delete_all_products_task(job_id):
    db: Session = SessionLocal()
    try:
        db.query(Product).delete()
        db.commit()
        update_progress(job_id, 100, "Deleted all products")
    except Exception as e:
        update_progress(job_id, -1, f"Error: {str(e)}")
    finally:
        db.close()
