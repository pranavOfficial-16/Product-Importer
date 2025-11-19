from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    event = Column(String(200), nullable=False)
    enabled = Column(Boolean, default=True)
