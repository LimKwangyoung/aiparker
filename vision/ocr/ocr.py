import cv2
import io
import os
from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Google Cloud Vision API 클라이언트 초기화
BASE_DIR = 'C:/Users/SSAFY/Desktop/Google Cloud Vision'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, 'AIPARKER.json')
client = vision.ImageAnnotatorClient()

def detect_text_from_frame(frame):
    # 프레임을 JPEG 포맷으로 인코딩
    success, encoded_image = cv2.imencode('.jpg', frame)
    if not success:
        return None

    # 이미지 바이트를 Google Vision API에 전송
    content = encoded_image.tobytes()
    image = vision.Image(content=content)

    # ImageContext 설정 (한국어 텍스트 우선)
    image_context = vision.ImageContext(
        language_hints=['ko']  # 'ko'는 한국어를 나타내는 언어 코드입니다.
    )

    # OCR 수행
    response = client.text_detection(image=image, image_context=image_context)
    texts = response.text_annotations

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))

    return texts[0].description if texts else None

def draw_text_on_image(frame, text):
    # OpenCV 이미지 프레임을 Pillow 이미지로 변환
    pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)

    # 원하는 폰트와 크기를 설정 (한글을 지원하는 TTF 폰트)
    font_path = "C:/Users/SSAFY/Desktop/Google Cloud Vision/NanumGothic.ttf"  # 예: 'NanumGothic.ttf'
    font = ImageFont.truetype(font_path, 30)

    # 텍스트를 이미지에 추가
    draw.text((10, 30), text, font=font, fill=(0, 255, 0))

    # Pillow 이미지를 다시 OpenCV 이미지로 변환
    frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return frame

# 웹캠을 열기
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임에서 텍스트 감지
    text = detect_text_from_frame(frame)
    
    # 텍스트가 감지되었으면 프레임에 표시
    if text:
        frame = draw_text_on_image(frame, text)

    # 프레임을 창에 표시
    cv2.imshow('Text Detection', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
