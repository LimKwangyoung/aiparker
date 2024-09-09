import os
import cv2

clicked_points = []
copied_image = None


def mouse_click(event, x, y, flags, param):
    # 왼쪽 마우스가 클릭되면 (x, y) 좌표 clicked_points 리스트에 저장
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((y, x))

        # 클릭한 점을 이미지에 표시
        image = copied_image.copy()
        for point in clicked_points:
            cv2.circle(image, (point[1], point[0]), 2, (255, 0, 0), thickness=20)
        cv2.imshow('image', image)


def main():
    """
    1번 CCTV의 판단 구역 : B2, B3, C2, C3
    2번 CCTV의 판단 구역 : B1, B2, C1. C2
    3번 CCTV의 판단 구역 : S1, S2, S3, A1, A2
    4번 CCTV의 판단 구역 : S4, E1, E2, A2, A3
    """

    global copied_image, clicked_points

    # 텍스트 파일 저장 디렉토리 경로
    txt_path = './SEGMENTATION'
    os.makedirs(txt_path, exist_ok=True)

    # 이미지 디렉토리 경로
    dir_path = './REGIONS'
    image_names = os.listdir(dir_path)

    # 새 윈도우 창을 만들고 그 윈도우 창에 mouse_click 콜백함수 설정
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('image', mouse_click)

    for image_name in image_names:
        image_path = f'{dir_path}/{image_name}'
        image = cv2.imread(image_path)

        copied_image = image.copy()

        # 프로그램 종료 플래그
        flag = False

        while True:
            cv2.imshow('image', image)
            key = cv2.waitKey(0)

            # 좌표 저장
            if key in (ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'),
                       ord('q'), ord('w'), ord('e'),
                       ord('a'), ord('s'), ord('d'),
                       ord('z'), ord('x'), ord('c')):
                # 좌표를 담은 텍스트 파일
                f = open(f'./{txt_path}/{image_name.split(".")[0]}.txt', 'a+')
                text_output = f'{image_name} {chr(key)}'
                for points in clicked_points:
                    text_output += f' ({points[0]},{points[1]})'
                text_output += '\n'
                f.write(text_output)

                clicked_points = []
                f.close()

            # 다음 사진으로 넘어가기
            if key == ord('n'):
                break

            # 프로그램 종료
            if key == ord('p'):
                flag = True
                break

        if flag:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
