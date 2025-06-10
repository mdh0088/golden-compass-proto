from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Content(Base):
    __tablename__ = "contents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # both, shorts_only, longform_only
    status = Column(String, default="pending")  # pending, processing, completed, failed
    progress = Column(Integer, default=0)

    # Results
    shorts_data = Column(JSON, default=list)
    longform_data = Column(JSON, default=dict)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())