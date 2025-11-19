from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/products", tags=["Products"])


# Get paginated products
@router.get("/")
def list_products(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    search: str = Query(None),
    active: bool = Query(None),
):
    query = db.query(Product)

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
            | Product.sku.ilike(f"%{search}%")
            | Product.description.ilike(f"%{search}%")
        )

    if active is not None:
        query = query.filter(Product.active == active)

    total = query.count()

    products = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "products": products,
    }


# Create product
@router.post("/")
def create_product(product: dict, db: Session = Depends(get_db)):
    new_product = Product(
        sku=product["sku"].lower(),
        name=product["name"],
        description=product["description"],
        price=product["price"],
        active=product.get("active", True),
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Update product
@router.put("/{sku}")
def update_product(sku: str, data: dict, db: Session = Depends(get_db)):
    sku = sku.lower()
    product = db.query(Product).filter(Product.sku == sku).first()

    if not product:
        return {"error": "Product not found"}

    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


# Delete product
@router.delete("/{sku}")
def delete_product(sku: str, db: Session = Depends(get_db)):
    sku = sku.lower()
    product = db.query(Product).filter(Product.sku == sku).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)
    db.commit()
    return {"message": "Deleted"}
