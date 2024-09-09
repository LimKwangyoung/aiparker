from gpiozero import DistanceSensor, Servo
from time import sleep

# 서보모터의 값을 직접 설정하고 잠시 후 비활성화하는 함수
def set_servo_value(value):
    servo.value = value
    sleep(1)
    servo.detach()

if __name__ == '__main__':
    # 초음파 센서 설정 (사용하지 않으므로 생략 가능)
    sensor = DistanceSensor(echo=23, trigger=24, max_distance=1, threshold_distance=0.2)

    # 서보모터 설정
    servo = Servo(18)
    
    # 차단기 초기화
    set_servo_value(-1)

    sleep(2)

    while True:
        # 사용자 입력 받기
        user_input = input("Enter 0 to close the barrier or 1 to open it: ")

        if user_input == "0":
            print("Closing the barrier...")
            set_servo_value(-1)  # 서보모터 값을 -1로 설정
        elif user_input == "1":
            print("Opening the barrier...")
            set_servo_value(1)  # 서보모터 값을 1로 설정
        else:
            print("Invalid input. Please enter 0 or 1.")
        
        # 잠시 대기 후 반복 (필요에 따라 조정)
        sleep(0.5)
