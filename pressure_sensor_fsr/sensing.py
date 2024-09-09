import spidev
import time
import RPi.GPIO as GPIO
from signal import pause
import time
import os
from time import sleep
from datetime import datetime
from dotenv import load_dotenv
from aws_iot import MQTTBuilder

# mqtt 변수
mqtt_build = None

# 토픽 설정
# CCTV 측에서 게시
## 라즈베리파이에 초음파와 압센서로 차량있는지 확인 요청
PARKED_REQUEST = "car/request-parked"

# CCTV 측에서 구독
## 라즈베리파이에서 차량 있는지 응답
PARKED_RESPONSE = "car/response-parked"

# SPI 초기화
spi = spidev.SpiDev()
try:
    spi.open(0, 0)  # 또는 spi.open(0, 1)로 시도
except FileNotFoundError:
    print("SPI 디바이스 파일을 찾을 수 없습니다. SPI 인터페이스가 활성화되었는지 확인하세요.")
    exit(1)

spi.max_speed_hz = 1350000

# GPIO 초기화
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# HC-SR04 초음파 센서 핀 설정
TRIG_PIN = 23
ECHO_PIN = 24
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# 상태 변수 초기화
parking_sensing_triggered = False

def read_adc(channel):
    if channel > 3 or channel < 0:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def read_distance():
    # Trig 핀을 LOW로 설정하여 짧은 시간 동안 초기화
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.5)

    # Trig 핀을 HIGH로 설정하여 초음파 신호 전송
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Echo 핀이 HIGH로 변할 때까지 대기
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Echo 핀이 LOW로 변할 때까지 대기
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Echo 핀이 HIGH로 유지된 시간 계산
    pulse_duration = pulse_end - pulse_start

    # 거리 계산 (음속: 34300 cm/s)
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

# MQTT 메시지 수신 콜백 함수 정의
def on_custom_message_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}': {payload.decode()}")

    # 영상처리로부터 확인해달라고 할 경우, 자리의 초음파 센서 확인하기
    if topic == PARKED_REQUEST:
        cnt = 0
        is_parking = False

        # 3초 동안 초음파 센서와 압력 센서 값 센싱
        while cnt < 15:
            sensor_value = read_adc(0)  # ADC0834의 0번 채널 읽기
            voltage = sensor_value * 3.3 / 1024
            distance = read_distance()  # HC-SR04 초음파 센서 거리 읽기
            print("FSR Sensor Value: {}, Voltage: {:.2f}V, Distance: {:.2f} cm".format(sensor_value, voltage, distance))

            # 조건 확인: 초음파 거리 7cm 이내 및 압력 센서 값 560 이상
            if distance <= 7 and sensor_value >= 30:
                print("Parking sensing!")
                is_parking = True
            
            cnt += 1
            sleep(0.1)
        
        if is_parking is True:
            mqtt_build.publish_message(PARKED_RESPONSE, 1)
        else:
            mqtt_build.publish_message(PARKED_RESPONSE, 0)



if __name__ == "__main__":
    load_dotenv()

    END_POINT = os.environ.get('END_POINT')
    CERT_FILE_PATH = os.environ.get('CERT_FILE_PATH')
    CA_FILE_PATH = os.environ.get('CA_FILE_PATH')
    PRI_KEY_FILE_PATH = os.environ.get('PRI_KEY_FILE_PATH')
    # MQTT_PORT = 8883
    MQTT_PORT = 8888

    # print(CERT_FILE_PATH)

    mqtt_build = MQTTBuilder() \
                .set_endpoint(END_POINT) \
                .set_port(MQTT_PORT) \
                .set_cert_filepath(CERT_FILE_PATH) \
                .set_ca_filepath(CA_FILE_PATH) \
                .set_pri_key_filepath(PRI_KEY_FILE_PATH) \
                .set_client_id("A104-rpi2") \
                .set_connection() \
                .set_message_callback(on_custom_message_received) \
                .add_topic(PARKED_REQUEST)

    while True:
        time.sleep(1)
    
    mqttBuild.set_disconnection()
