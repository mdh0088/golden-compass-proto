from celery import current_task
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.content import Content
from app.services.ai_client import AIClient
from app.services.video_creator import VideoCreator
from app.core.config import settings
import asyncio
import os


@celery_app.task(bind=True)
def generate_content_task(self, content_id: str):
    """콘텐츠 생성 메인 태스크"""
    db = SessionLocal()
    ai_client = AIClient()
    video_creator = VideoCreator()

    try:
        # 콘텐츠 정보 조회
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            return {"error": "Content not found"}

        # 상태 업데이트
        content.status = "processing"
        db.commit()

        # 디렉토리 생성
        os.makedirs(settings.SHORTS_PATH, exist_ok=True)
        os.makedirs(settings.LONGFORM_PATH, exist_ok=True)
        os.makedirs(settings.THUMBNAILS_PATH, exist_ok=True)

        results = {"shorts": [], "longform": None}

        # 1. 숏츠 생성 (10개)
        if content.content_type in ["both", "shorts_only"]:
            shorts_data = []

            for i in range(1, 11):
                # 진행률 업데이트
                progress = int((i / 11) * 50)
                current_task.update_state(
                    state='PROGRESS',
                    meta={'current': i, 'total': 11, 'progress': progress}
                )

                # 스크립트 생성
                script_data = asyncio.run(
                    ai_client.generate_short_script(content.topic, i)
                )

                # 음성 생성
                audio_path = settings.SHORTS_PATH / f"short_{content_id}_{i}_audio.mp3"
                asyncio.run(
                    ai_client.generate_voice(script_data['script'], str(audio_path))
                )

                # 비디오 생성
                video_path = settings.SHORTS_PATH / f"short_{content_id}_{i}.mp4"
                video_creator.create_short_video(
                    script_data,
                    str(audio_path),
                    str(video_path)
                )

                short_result = {
                    "id": f"{content_id}_short_{i}",
                    "title": script_data['title'],
                    "duration": script_data['duration'],
                    "file_url": f"/media/shorts/{video_path.name}"
                }

                shorts_data.append(script_data)
                results["shorts"].append(short_result)

            content.shorts_data = results["shorts"]

        # 2. 롱폼 생성 (1개)
        if content.content_type in ["both", "longform_only"]:
            # 진행률 업데이트
            current_task.update_state(
                state='PROGRESS',
                meta={'current': 'longform', 'total': 'final', 'progress': 75}
            )

            # 롱폼 스크립트 생성
            longform_data = asyncio.run(
                ai_client.generate_longform_script(content.topic, shorts_data if 'shorts_data' in locals() else [])
            )

            # 음성 생성
            audio_path = settings.LONGFORM_PATH / f"long_{content_id}_audio.mp3"
            asyncio.run(
                ai_client.generate_voice(longform_data['script'], str(audio_path))
            )

            # 비디오 생성
            video_path = settings.LONGFORM_PATH / f"long_{content_id}.mp4"
            video_creator.create_longform_video(
                longform_data,
                str(audio_path),
                str(video_path)
            )

            results["longform"] = {
                "id": f"{content_id}_long",
                "title": longform_data['title'],
                "duration": longform_data['duration'],
                "file_url": f"/media/longform/{video_path.name}"
            }

            content.longform_data = results["longform"]

        # 완료 처리
        content.status = "completed"
        content.progress = 100
        db.commit()

        return {
            "status": "completed",
            "results": results
        }

    except Exception as e:
        content.status = "failed"
        db.commit()
        raise e
    finally:
        db.close()