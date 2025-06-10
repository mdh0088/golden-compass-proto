from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import os


class VideoCreator:
    def __init__(self):
        self.font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 한글 폰트

    def create_thumbnail(self, title: str, output_path: str) -> str:
        """썸네일 생성"""
        # 1920x1080 크기의 황금색 배경
        img = Image.new('RGB', (1920, 1080), color='#FFD700')
        draw = ImageDraw.Draw(img)

        # 제목 추가
        try:
            font = ImageFont.truetype(self.font_path, 80)
        except:
            font = ImageFont.load_default()

        # 텍스트를 중앙에 배치
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1920 - text_width) // 2
        y = (1080 - text_height) // 2

        # 검은색 테두리
        for adj_x in [-2, 0, 2]:
            for adj_y in [-2, 0, 2]:
                draw.text((x + adj_x, y + adj_y), title, font=font, fill='black')

        # 흰색 텍스트
        draw.text((x, y), title, font=font, fill='white')

        img.save(output_path)
        return output_path

    def create_short_video(self, data: dict, audio_path: str, output_path: str) -> str:
        """숏츠 비디오 생성 (9:16 세로형)"""
        # 썸네일을 비디오 배경으로 사용
        thumbnail_path = output_path.replace('.mp4', '_thumb.jpg')
        self.create_thumbnail(data['title'], thumbnail_path)

        # 오디오 로드
        audio = AudioFileClip(audio_path)
        duration = audio.duration

        # 이미지를 비디오로 변환 (1080x1920 세로형)
        img = Image.open(thumbnail_path).resize((1080, 1920))
        img_array = np.array(img)
        video = ImageClip(img_array, duration=duration)

        # 자막 추가
        subtitle = TextClip(
            data['script'][:100] + "...",
            fontsize=40,
            color='white',
            font=self.font_path,
            size=(900, None),
            method='caption'
        ).set_position(('center', 'bottom')).set_duration(duration)

        # 합성
        final = CompositeVideoClip([video, subtitle])
        final = final.set_audio(audio)

        # 저장
        final.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30
        )

        return output_path

    def create_longform_video(self, data: dict, audio_path: str, output_path: str) -> str:
        """롱폼 비디오 생성 (16:9 가로형)"""
        # 썸네일 생성
        thumbnail_path = output_path.replace('.mp4', '_thumb.jpg')
        self.create_thumbnail(data['title'], thumbnail_path)

        # 오디오 로드
        audio = AudioFileClip(audio_path)
        duration = min(audio.duration, settings.LONGFORM_DURATION)

        # 기본 배경 (1920x1080)
        img = Image.open(thumbnail_path)
        img_array = np.array(img)
        video = ImageClip(img_array, duration=duration)

        # 간단한 텍스트 오버레이
        title_clip = TextClip(
            data['title'],
            fontsize=60,
            color='white',
            font=self.font_path
        ).set_position('center').set_duration(5)

        # 합성
        final = CompositeVideoClip([video, title_clip])
        final = final.set_audio(audio)

        # 저장
        final.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30
        )

        return output_path