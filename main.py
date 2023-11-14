import os
import cv2
from colorama import Fore, Style, init


def error(text):
    print(f"{Fore.RED}{Style.BRIGHT}{text}")

def success(result):
    if result:
        print(f"Результат: {Fore.GREEN}{Style.BRIGHT}{result}")


def get_color_name(color):
    color_type = list(color).index(max(color))
    if color_type == 0:
        return "B"
    elif color_type == 1:
        return "G"
    else:
        return "R"
    

def recognize_tags(image, thresholded_image, filter_funtion, names):
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(filter(filter_funtion, contours))

    for contour in contours:
        M = cv2.moments(contour)
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])

        color_name = get_color_name(image[center_y, center_x])
        names.append(color_name)

        cv2.circle(image, (center_x, center_y), 7, (255, 255, 255), -1)

        cv2.putText(image, f"{color_name}{names.count(color_name)}", (center_x - 20, center_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 4)

    image = cv2.drawContours(image, contours, -1, (255, 255, 255), 3)


def task1():
    assets_path = input(f"Введите путь до папки: ")

    if not os.path.isabs(assets_path):
        assets_path = os.path.join(os.getcwd(), assets_path)

    if not os.path.isdir(assets_path):
        error("Путь не является папкой!")
        return

    assets = os.listdir(assets_path)
    colors = []
    for asset in assets:
        image = cv2.imread(f"{assets_path}\\{asset}")
        colors.append(get_color_name(image[0, 0]))

    return "".join(colors)


def task2():
    def filter_contours(contour):
        area = cv2.contourArea(contour)
        return area > 1000 and area <= 1000000

    assets_path = "Task 2/"
    asset = os.listdir(assets_path)[0]

    image = cv2.imread(f"{assets_path}\\{asset}")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded_image = cv2.threshold(gray_image, 110, 255, 0)

    names = []
    recognize_tags(image, thresholded_image, filter_contours, names)

    cv2.imshow(asset, image)
    cv2.waitKey(0)
    cv2.imwrite(f"{assets_path}\\SUCCESS_{asset}", image)


def task3():
    def filter_contours(contour):
        area = cv2.contourArea(contour)
        return area > 1000 and area <= 90000

    assets_path = "Task 3/"
    asset = os.listdir(assets_path)[0]

    capture = cv2.VideoCapture(f"{assets_path}\\{asset}")
    if not capture.isOpened():
        error("Ошибка открытия видео!")

    while capture.isOpened() and cv2.waitKey(25) & 0xFF != ord('q'):
        success, frame = capture.read()
        if success:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresholded_frame = cv2.threshold(gray_frame, 100, 255, 0)
            contours, _ = cv2.findContours(thresholded_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = list(filter(filter_contours, contours))

            names = []
            recognize_tags(frame, thresholded_frame, filter_contours, names)

            cv2.imshow(asset, frame)
            cv2.waitKey(0)
            print(names)
            continue
        break

    capture.release()


if __name__ == "__main__":
    init(autoreset=True)
    scope = globals()

    task = "task" + input(f"Какое задание выполнить? ")

    if task in scope:
        success(scope[task]())
    else:
        error("Такого задания нет!")
