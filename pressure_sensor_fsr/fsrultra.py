import spidev
import time
import RPi.GPIO as GPIO

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

while True:
    sensor_value = read_adc(0)  # ADC0834의 0번 채널 읽기
    voltage = sensor_value * 3.3 / 1024
    distance = read_distance()  # HC-SR04 초음파 센서 거리 읽기
    print("FSR Sensor Value: {}, Voltage: {:.2f}V, Distance: {:.2f} cm".format(sensor_value, voltage, distance))

    # 조건 확인: 초음파 거리 7cm 이내 및 압력 센서 값 560 이상
    if distance <= 7 and sensor_value >= 30:
        if not parking_sensing_triggered:
            print("Parking sensing!")
            parking_sensing_triggered = True
    else:
        parking_sensing_triggered = False

    time.sleep(0.1)
