import openai
from elevenlabs import generate, Voice
from app.core.config import settings
import asyncio


class AIClient:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def generate_short_script(self, topic: str, index: int) -> dict:
        """숏츠용 30초 스크립트 생성"""
        prompt = f"""
        황금나침반 채널의 {index}번째 숏츠 스크립트를 작성해주세요.
        주제: {topic}
        길이: 30초 (약 150-200자)

        구조:
        1. 첫 3초 훅: 충격적인 질문이나 호기심 자극
        2. 메인 내용: 재물운 정보
        3. 마지막 3초: 행동 유도

        톤: 친근하면서도 신비로운 느낌
        반드시 "황금나침반"을 언급하세요.
        """

        response = await asyncio.to_thread(
            openai.chat.completions.create,
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        script = response.choices[0].message.content

        # 제목 생성
        title_prompt = f"다음 스크립트의 매력적인 YouTube 숏츠 제목을 만들어주세요 (10자 이내): {script}"
        title_response = await asyncio.to_thread(
            openai.chat.completions.create,
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": title_prompt}],
            max_tokens=50
        )

        return {
            "index": index,
            "title": title_response.choices[0].message.content.strip(),
            "script": script,
            "duration": settings.SHORT_DURATION
        }

    async def generate_longform_script(self, topic: str, shorts_data: list) -> dict:
        """롱폼용 10분 스크립트 생성"""
        shorts_summary = "\n".join([f"- {s['title']}: {s['script'][:50]}..." for s in shorts_data])

        prompt = f"""
        황금나침반 채널의 10분 롱폼 영상 스크립트를 작성해주세요.
        주제: {topic}

        참고할 숏츠 내용:
        {shorts_summary}

        구조:
        1. 인트로 (30초): 채널 소개 + 오늘의 주제
        2. 전체 운세 개요 (2분): {topic}의 전반적인 흐름
        3. 12띠별 상세 분석 (6분): 각 띠별 30초씩 상세 설명
        4. 특별 조언 (1분): 재물운 극대화 방법
        5. 마무리 (30초): 구독 유도 + 다음 영상 예고

        톤: 전문적이면서도 따뜻한 느낌
        약 3000자 분량으로 작성해주세요.
        """

        response = await asyncio.to_thread(
            openai.chat.completions.create,
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )

        return {
            "title": f"[황금나침반] {topic} 완벽 가이드",
            "script": response.choices[0].message.content,
            "duration": settings.LONGFORM_DURATION
        }

    async def generate_voice(self, text: str, output_path: str) -> str:
        """ElevenLabs로 음성 생성"""
        audio = await asyncio.to_thread(
            generate,
            text=text,
            voice=Voice(voice_id=settings.ELEVENLABS_VOICE_ID),
            model="eleven_multilingual_v2"
        )

        with open(output_path, "wb") as f:
            f.write(audio)

        return output_path