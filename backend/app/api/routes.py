from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.content import Content
from app.services.tasks import generate_content_task
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()


class ContentGenerateRequest(BaseModel):
    topic: str
    content_type: str = "both"  # both, shorts_only, longform_only


class ContentGenerateResponse(BaseModel):
    task_id: str
    status: str


@router.post("/content/generate", response_model=ContentGenerateResponse)
async def generate_content(
        request: ContentGenerateRequest,
        db: Session = Depends(get_db)
):
    """콘텐츠 생성 요청"""
    # DB에 콘텐츠 생성
    content = Content(
        topic=request.topic,
        content_type=request.content_type,
        status="pending"
    )
    db.add(content)
    db.commit()
    db.refresh(content)

    # Celery 태스크 시작
    task = generate_content_task.delay(content.id)

    return ContentGenerateResponse(
        task_id=content.id,
        status="processing"
    )


@router.get("/content/status/{task_id}")
async def get_content_status(
        task_id: str,
        db: Session = Depends(get_db)
):
    """콘텐츠 생성 상태 확인"""
    content = db.query(Content).filter(Content.id == task_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return {
        "task_id": content.id,
        "status": content.status,
        "progress": content.progress,
        "results": {
            "shorts": content.shorts_data or [],
            "longform": content.longform_data or None
        }
    }


@router.get("/content/list")
async def list_contents(
        db: Session = Depends(get_db)
):
    """생성된 콘텐츠 목록"""
    contents = db.query(Content).order_by(Content.created_at.desc()).all()

    return {
        "contents": [
            {
                "id": c.id,
                "topic": c.topic,
                "created_at": c.created_at.isoformat(),
                "status": c.status,
                "shorts_count": len(c.shorts_data) if c.shorts_data else 0,
                "has_longform": bool(c.longform_data)
            }
            for c in contents
        ]
    }