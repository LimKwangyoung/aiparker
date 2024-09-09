import os
import sys
import json
import time
from pathlib import Path
import cv2
import collections
from shapely.geometry import Polygon
from dotenv import load_dotenv
from aws_iot import MQTTBuilder
import mysql.connector
from mysql.connector import errorcode

from ultralytics.utils.plotting import colors
from utils.general import check_requirements
import detect
import download

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# mqtt 변수
mqtt_build = None

# 토픽 설정
# CCTV 측에서 게시
## 라즈베리파이에 초음파와 압센서로 차량있는지 확인 요청
PARKED_REQUEST = "car/request-parked"

# CCTV 측에서 구독
## 라즈베리파이에서 차량 있는지 응답
PARKED_RESPONSE = "car/response-parked"

# 라즈베리파이가 응답했는지 확인하는 플래그
get_response = False

final_result = {}

# 주차 구역
REGION = {
    '1': 'S1', '2': 'S2', '3': 'S3', '4': 'S4', '5': 'E1', '6': 'E2',
    'q': 'A1', 'w': 'A2', 'e': 'A3',
    'a': 'B1', 's': 'B2', 'd': 'B3',
    'z': 'C1', 'x': 'C2', 'c': 'C3'
}


# MySQL 연결 함수
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

# 주차 정보를 MySQL에 업데이트하는 함수
def update_parking_spots(final_result):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for code, is_here in final_result.items():
            sql = "UPDATE ParkingSpot SET isHere=%s WHERE code=%s"
            cursor.execute(sql, (is_here, code))

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# MQTT 메시지 수신 콜백 함수 정의
def on_custom_message_received(topic, payload, dup, qos, retain, **kwargs):
    global get_response
    print(f"Received message from topic '{topic}': {payload.decode()}")

    if topic == PARKED_RESPONSE:
        response_str = payload.decode().strip('"')  # 따옴표 제거
        try:
            response = int(response_str)  # 문자열을 정수로 변환
            final_result['A1'] = response
            get_response = True
            print("Updated final result with A2 response:", final_result)
        except ValueError as e:
            print(f"Error converting payload to int: {e}")


def main(car_thd_1=0.75, car_thd_2=0.25, is_draw=False):
    """
    1번 CCTV의 판단 구역 : B2, B3, C2, C3
    2번 CCTV의 판단 구역 : B1, B2, C1. C2
    3번 CCTV의 판단 구역 : S1, S2, S3, A1, A2
    4번 CCTV의 판단 구역 : S4, E1, E2, A2, A3
    """

    def run(image_path):
        # CCTV 테스트 이미지
        test_image = cv2.imread(image_path)

        if is_draw:
            for region, region_info in cctv_dict[cctv_num].items():
                for idx in range(len(region_info)):
                    cv2.line(test_image, region_info[idx], region_info[(idx + 1) % len(region_info)],
                             color=(0, 0, 255), thickness=10)

        # Object Detection Confidence 값과 좌표값
        # check_requirements(ROOT / "requirements.txt", exclude=("tensorboard", "thop"))
        prediction = detect.run(
            weights='./runs/best.pt',
            source=image_path,
            nosave=True,
        )

        for pred_idx in range(0, len(prediction), 3):
            cls = int(prediction[pred_idx])
            boxes = list(map(int, prediction[pred_idx + 2]))

            if cls in (1, 6):
                # 차량
                if cls == 1:
                    polygon_boxes = Polygon([
                        (boxes[0], boxes[1]), (boxes[0], boxes[3]),
                        (boxes[2], boxes[3]), (boxes[2], boxes[1])
                    ])

                    # 주차 구역별 다각형과 객체 사각형의 넓이
                    for region, info in region_dict.items():
                        if cctv_num in info:
                            polygon_parking = Polygon(info[cctv_num])
                            intersection = polygon_boxes.intersection(polygon_parking)

                            if intersection.area / polygon_parking.area >= car_thd_2:
                                parking[region].append(intersection.area / polygon_parking.area)

                # 주차 금지 표지판
                else:
                    polygon_boxes = Polygon([
                        (boxes[0], boxes[1]), (boxes[0], boxes[3]),
                        (boxes[2], boxes[3]), (boxes[2], boxes[1])
                    ])

                    # 주차 구역별 다각형과 객체 사각형의 넓이
                    for region, info in region_dict.items():
                        if cctv_num in info:
                            polygon_parking = Polygon(info[cctv_num])
                            intersection = polygon_boxes.intersection(polygon_parking)

                            sign[region].append(intersection.area / polygon_parking.area)

            if is_draw:
                cv2.rectangle(test_image, (boxes[0], boxes[1]), (boxes[2], boxes[3]),
                              color=colors(cls, True), thickness=10)

        if is_draw:
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.imshow('image', test_image)
            cv2.waitKey(0)

    # 주차 구역 별 좌표 저장
    region_dict = collections.defaultdict(dict)

    # CCTV 별 좌표 저장
    cctv_dict = collections.defaultdict(dict)

    for cctv_num in ('1', '2'):
        f = open(f'./SEGMENTATION/{cctv_num}.txt')
        while True:
            line = f.readline().strip()
            if not line:
                break

            # 정수와 좌표 형태로 전처리
            line = line.split()
            for i in range(2, len(line)):
                tmp = line[i].split(',')
                line[i] = tuple([int(tmp[1][:-1]), int(tmp[0][1:])])
            region_dict[REGION[line[1]]][line[0][:-4]] = line[2:]
            cctv_dict[line[0][:-4]][REGION[line[1]]] = line[2:]

    # 주차 구역 별 차량 확률
    parking = collections.defaultdict(list)

    # 주차 구역 별 주차 금지 표지판 확률
    sign = collections.defaultdict(list)

    # 최근 이미지의 주차 판별
    for cctv_num in ('1', '2'):
        # S3
        latest_path = download.main(f'./CCTVS/{cctv_num}')
        run(image_path=f'./CCTVS/{cctv_num}/{latest_path}')

        # local
        # images = os.listdir(f'./CCTVS/{cctv_num}')
        # run(image_path=f'./CCTVS/{cctv_num}/{images[0]}')

    # 주차 불가능 구역
    result = []
    for region_name, prob_lst in parking.items():
        if min(prob_lst) >= car_thd_1:
            result.append(region_name)

    for region_name, prob_lst in sign.items():
        if min(prob_lst) > 0:
            result.append(region_name)
    
    return result

def result_to_json(result):
    all_regions = ['S1', 'S2', 'S3', 'S4', 'E1', 'E2', 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
    json_result = {region: 1 if region in result else 0 for region in all_regions}
    return json_result

if __name__ == '__main__':
    load_dotenv()

    END_POINT = os.environ.get('END_POINT')
    CERT_FILE_PATH = os.environ.get('CERT_FILE_PATH')
    CA_FILE_PATH = os.environ.get('CA_FILE_PATH')
    PRI_KEY_FILE_PATH = os.environ.get('PRI_KEY_FILE_PATH')
    MQTT_PORT = 8883

    mqtt_build = MQTTBuilder() \
                .set_endpoint(END_POINT) \
                .set_port(MQTT_PORT) \
                .set_cert_filepath(CERT_FILE_PATH) \
                .set_ca_filepath(CA_FILE_PATH) \
                .set_pri_key_filepath(PRI_KEY_FILE_PATH) \
                .set_client_id("A104-CCTV") \
                .set_connection() \
                .set_message_callback(on_custom_message_received) \
                .add_topic(PARKED_RESPONSE)

    while True:
        # 현재 CCTV 상태 영상처리
        result = main(is_draw=False)
        print("Parking result:", result)

        json_result = result_to_json(result)
        print("JSON result:", json.dumps(json_result, indent=4))

        final_result = json_result

        # # A1 구역이 비어있는 경우 2차로 확인해달라서 요청
        # if json_result['A1'] == 0:
        #     mqtt_build.publish_message(PARKED_REQUEST, "check the area")

        #     # 응답받을때까지 대기
        #     while get_response is False:
        #         time.sleep(1)

        # 최종 결과
        print("최종 결과 : ")
        print(final_result)
        get_response = False

        # mySQL에 저장
        update_parking_spots(final_result)

        time.sleep(60)

    mqtt_build.set_disconnection()
