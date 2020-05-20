import numpy as np
from PIL import ImageGrab
import cv2


white = ([255, 255, 255])
blue = ([255, 0, 0])
red = ([0, 0, 255])
green = ([0, 255, 0])


def process_screen_canny_edge(original_screen, print_slope, show_raw_image, detected_lane_color):
    processed_image = cv2.cvtColor(original_screen, cv2.COLOR_BGR2RGB)
    yellow_to_white(processed_image)
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image,
                                threshold1=100,
                                threshold2=110)
    processed_image = cv2.GaussianBlur(processed_image, (5, 5), 0)
    processed_image = region_of_interest(processed_image)
    solid_outside_lines = cv2.HoughLinesP(processed_image,
                                          rho=1,
                                          theta=np.pi / 180,
                                          threshold=300,
                                          minLineLength=220,
                                          maxLineGap=2)

    if show_raw_image is True:
        draw_lines(processed_image, solid_outside_lines, print_slope=print_slope, color=([255, 255, 255]))
        return processed_image
    else:
        processed_image = cv2.cvtColor(original_screen, cv2.COLOR_BGR2RGB)
        draw_lines(processed_image, solid_outside_lines, print_slope=print_slope, color=detected_lane_color)
        return processed_image


def region_of_interest(image):
    vertices = np.array([
        [0, 480],
        [410, 300],
        [520, 300],
        [958, 480],
        [958, 737],
        [0, 737]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, [vertices], 255)
    masked = cv2.bitwise_and(image, mask)
    return masked


def yellow_to_white(image):
    # Fine Tuning of detection of yellow lines.
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(image_hsv, np.array([40, 50, 180]), np.array([140, 150, 255]))
    image[mask > 0] = (255, 255, 255)
    return image


def draw_lines(image, lines, color, print_slope):
    if color == 0:
        color = white
    elif color == 1:
        color = blue
    elif color == 2:
        color = red
    elif color == 3:
        color = green
    else:
        # Defaults to white.
        color = white

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            if print_slope is True:
                print('Slope for line {} = {}'.format([x1, y1, x2, y2], round(slope, 2)))
            if -0.1 < slope < 0.1:
                continue

            cv2.line(image, (x1, y1), (x2, y2), color, thickness=10)
