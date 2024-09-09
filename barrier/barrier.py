from gpiozero import DistanceSensor, Servo
from signal import pause
from picamera2 import Picamera2
import time
from time import sleep
from datetime import datetime
import os
import subprocess
from dotenv import load_dotenv
from aws_iot import MQTTBuilder

# 현재 진행중인 차가 있는지 저장하는 변수
is_passing = False

# mqtt 변수
mqtt_build = None

# 토픽 설정
# 라즈베리파이에서 퍼블리싱
## 차량 감지하고 사진 찍어서 업로드 후 ec2에 보낼 토픽
CAR_PHOTO_UPLOAD = "car/photo-upload"

# 라즈베리파이에서 구독
## 서버가 차단기 열라고 요청하는 토픽
OPEN_REQUEST = "car/open"


# 사진 촬영 후 저장 및 S3 업로드
def save_image():
    output_file = None

    try:
        picam2.start()
        print("사진 촬영")
        sleep(1)

        # 현재 시간을 파일 이름에 포함
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{current_time}.jpg"
        output_file = os.path.join(save_folder, f"{current_time}.jpg")

        output = picam2.capture_image()
        output.save(output_file)
        # print(f"Image saved as: {output_file}")

        # S3에 업로드
        subprocess.run(["./upload_s3.sh", output_file])

        sleep(2)
    
    finally:
        picam2.stop()
    
    return file_name


# 물체가 20cm 이내로 감지되었을 때 서보모터를 최대 값으로 설정 및 MQTT 메시지 퍼블리싱
def object_in_range():
    global is_passing
    if is_passing is False:
        is_passing = True

        # 사진 촬영 후 저장
        file_name = save_image()

        # 차량 사진 업로드했다고 전송
        mqtt_build.publish_message(CAR_PHOTO_UPLOAD, file_name)


# 물체가 없을 때 차단기 닫기
def object_out_of_range():
    global is_passing
    if is_passing is True:
        set_servo_value(-1)
        sleep(1)
        is_passing = False
        print("차단기 close")

# 서보모터의 값을 직접 설정하고 잠시 후 비활성화하는 함수
def set_servo_value(value):
    servo.value = value
    sleep(1)
    servo.detach()

# 차가 있는지 계속해서 감지
def wait_for_passing():
    while True:
        sleep(1)
        if sensor.distance >= 0.3:
            object_out_of_range()
            break

# MQTT 메시지 수신 콜백 함수 정의
def on_custom_message_received(topic, payload, dup, qos, retain, **kwargs):
    global is_passing
    print(f"Received message from topic '{topic}': {payload.decode()}")
    if topic == OPEN_REQUEST:
        set_servo_value(1)
        cnt = 10
        while cnt <= 10:
            print(f"현재 {cnt}초")
            print(f"현재 차량 진행 중 :{is_passing}")
            time.sleep(1)
            cnt -= 1
            if cnt == 0:
                break
        wait_for_passing()

if __name__ == '__main__':
    
    load_dotenv()

    END_POINT = os.environ.get('END_POINT')
    CERT_FILE_PATH = os.environ.get('CERT_FILE_PATH')
    CA_FILE_PATH = os.environ.get('CA_FILE_PATH')
    PRI_KEY_FILE_PATH = os.environ.get('PRI_KEY_FILE_PATH')
    MQTT_PORT = 8883

    # print(CERT_FILE_PATH)

    mqtt_build = MQTTBuilder() \
                .set_endpoint(END_POINT) \
                .set_port(MQTT_PORT) \
                .set_cert_filepath(CERT_FILE_PATH) \
                .set_ca_filepath(CA_FILE_PATH) \
                .set_pri_key_filepath(PRI_KEY_FILE_PATH) \
                .set_client_id("A104-rpi") \
                .set_connection() \
                .set_message_callback(on_custom_message_received) \
                .add_topic(OPEN_REQUEST)

    ## 초음파 센서 설정
    sensor = DistanceSensor(echo=23, trigger=24, max_distance=1, threshold_distance=0.2)

    # 서보모터 설정
    servo = Servo(18)

    # 카메라 설정
    picam2 = Picamera2()
    config = picam2.create_preview_configuration()
    picam2.configure(config)

    # 사진을 저장할 폴더 경로
    save_folder = "images"

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    # 차단기 초기화
    set_servo_value(-1)

    # 초음파 센서 이벤트 핸들러 설정
    sensor.when_in_range = object_in_range
    #sensor.when_out_of_range = object_out_of_range


    # 프로그램이 종료되지 않도록 pause
    pause()
    

    while True:
        time.sleep(1)

    mqttBuild.set_disconnection()
