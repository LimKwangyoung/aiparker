# -*- coding: utf-8 -*-

import time
from time import sleep
from datetime import datetime
import os
import subprocess
from dotenv import load_dotenv
from aws_iot import MQTTBuilder
from google.cloud import vision
import io
import os
from PIL import Image
import mysql.connector
from mysql.connector import errorcode


# mqtt 변수
mqtt_build = None

# 퍼블리싱 메시지
open_request = "open barrier"

# 토픽 설정
# 라즈베리파이에서 퍼블리싱
## 차량 감지하고 사진 찍어서 업로드 후 ec2에 보낼 토픽
CAR_PHOTO_UPLOAD = "car/photo-upload"

# 라즈베리파이에서 구독
## 서버가 차단기 열라고 요청하는 토픽
OPEN_REQUEST = "car/open"

# Define the crop box (left, upper, right, lower)
crop_box = (200, 230, 400, 450)  # Adjust this according to your needs

# MySQL 연결 함수
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user = os.getenv("MYSQL_USER"),
            password = os.getenv("MYSQL_PASSWORD"),
            host = os.getenv("MYSQL_HOST"),
            database = os.getenv("MYSQL_DATABASE")
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

# 데이터 삽입 함수
def insert_vehicle_entry(license_plate, entry_time, s3_link):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO Vehicle (licensePlate, type, entryTime, s3)
            VALUES (%s, %s, %s, %s)
        """, (license_plate, '일반', entry_time, s3_link))
        
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# OCR 위한 이미지 크롭
def crop_image(input_path, output_path, crop_box):
    with Image.open(input_path) as img:
        cropped_img = img.crop(crop_box).resize((600, 600))
        cropped_img.save(output_path)

# google vision API 사용해서 OCR
def detect_text(img_name, crop_box=None):
    BASE_DIR = '/home/ubuntu/AWSIoT'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, 'cert/AIPARKER.json')
    client = vision.ImageAnnotatorClient()

    input_path = os.path.join(BASE_DIR, 'incar_images', img_name)
    cropped_img_path = os.path.join(BASE_DIR, 'incar_images', 'cropped_' + img_name)
    
    if crop_box:
        crop_image(input_path, cropped_img_path, crop_box)
        path = cropped_img_path
    else:
        path = input_path

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    # Define image context with language hints
    image_context = vision.ImageContext(
        language_hints=['ko']  # 'ko' is the language code for Korean
    )

    response = client.text_detection(image=image, image_context=image_context)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return texts[0].description if texts else None

# 쌍따옴표 제거 함수
def remove_quotes(input_string):
    return input_string.replace('"', '')

# MQTT 메시지 수신 콜백 함수 정의
def on_custom_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("--------------------------------------------------------------")
    print(f"Received message from topic '{topic}': {payload.decode()}")
    
    if topic == CAR_PHOTO_UPLOAD:
        subprocess.run(["./download_s3.sh"])
        print("download images")
        sleep(2)
        
        # 이미지 정보 출력
        print("payload: " + remove_quotes(payload.decode()))
        print("ocr 실행")
        
        # Google OCR
        # Call the function with cropping
        text = detect_text(remove_quotes(payload.decode()))
        print(f"{text} 차량 정보 저장...")
        
        # 입차 시간 생성
        entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # S3 링크 생성
        s3_link = f"https://demo-bucket-1222.s3.ap-northeast-2.amazonaws.com/images/{remove_quotes(payload.decode())}"
        
        # 데이터 베이스에 저장
        insert_vehicle_entry(text, entry_time, s3_link)
        
        
        mqtt_build.publish_message(OPEN_REQUEST, open_request)


if __name__ == '__main__':

    load_dotenv()
    
    # 경로 설정
    END_POINT = os.environ.get('END_POINT')
    CERT_FILE_PATH = os.environ.get('CERT_FILE_PATH')
    CA_FILE_PATH = os.environ.get('CA_FILE_PATH')
    PRI_KEY_FILE_PATH = os.environ.get('PRI_KEY_FILE_PATH')
    MQTT_PORT = 8883

    
    # mqtt 빌드
    mqtt_build = MQTTBuilder() \
                .set_endpoint(END_POINT) \
                .set_port(MQTT_PORT) \
                .set_cert_filepath(CERT_FILE_PATH) \
                .set_ca_filepath(CA_FILE_PATH) \
                .set_pri_key_filepath(PRI_KEY_FILE_PATH) \
                .set_client_id("A104-ec2") \
                .set_connection() \
                .set_message_callback(on_custom_message_received) \
                .add_topic(CAR_PHOTO_UPLOAD)


    while True:
        time.sleep(1)
        

    mqttBuild.set_disconnection()