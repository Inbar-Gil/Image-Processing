import cv2
import numpy as np
from average_color_finder import average_color_finder
from FRUIT_COLORS import *

WIN_RAT = 16 / 9
WIN_HEIGHT = 240
WIN_WIDTH = int(WIN_HEIGHT * WIN_RAT)
WIN_LOC1 = [0, 0]
WIN_LOC2 = [WIN_WIDTH, 0]
WIN_LOC3 = [WIN_WIDTH * 2, 0]
WIN_LOC4 = [0, WIN_HEIGHT]
WIN_LOC5 = [WIN_WIDTH, WIN_HEIGHT]
WIN_LOC6 = [2 * WIN_WIDTH, WIN_HEIGHT]
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT
BLANK_IMAGE = cv2.imread('Blank_Image.png')
cv2.imshow("TEST", BLANK_IMAGE)
BLANK_IMAGE_GRAY = cv2.cvtColor(BLANK_IMAGE, cv2.COLOR_BGR2GRAY)
BANNED_AREA = [[[-1, -1], [256, 72]], [[-1, 144], [20, 133]], [[256, 144], [180, 134]]]
THRESH = 20
IMAGE = cv2.imread('LIME655.png')
COLOR_SIMILARITY = 100
FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SCALE = 1
THICKNESS = 1
FONT_COLOR = (0, 0, 255)


def find_fruit(image, background):
    # edits an image using grayscale, morphology and contours
    initial_image = image.copy()
    gray_fig = show_grayscale_img(image)
    diff = show_diff_img(gray_fig, background)
    diff = show_threshed_img(diff)
    opening, fruit_locs = eliminate_noise(diff, it_close=3, it_open=1)
    non_zero_area = cv2.findNonZero(opening)
    contours, centers = add_contours(image, initial_image, opening)
    add_fruit_type(image, initial_image, contours, non_zero_area, centers)
    update = show_final_image(image, 0)
    return update, fruit_locs, contours


def find_min_max_vals(list_3d):
    # finds the min max values of a 2d list contained in a 3d list
    x = np.zeros(len(list_3d))
    y = np.zeros(len(list_3d))
    for i in range(len(list_3d)):
        pos_x = list_3d[i][0][0]
        pos_y = list_3d[i][0][1]
        if not check_banned_areas(pos_x, pos_y):
            x[i] = pos_x
            y[i] = pos_y
        else:
            x[i] = None
            y[i] = None
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if len(x) > 0:
        return int(min(x)), int(min(y)), int(max(x)), int(max(y))
    else:
        return None


def check_banned_areas(x, y):
    # confirms points are in allowed areas
    for rect in BANNED_AREA:
        if check_in_rectangle(rect[0], rect[1], x, y):
            return True
    return False


def check_in_rectangle(rect_start, rect_end, x, y):
    # checks if a point is in a rectangle
    x_start = min(rect_start[0], rect_end[0])
    x_end = max(rect_start[0], rect_end[0])
    y_start = min(rect_start[1], rect_end[1])
    y_end = max(rect_start[1], rect_end[1])
    return x_start < x < x_end and y_start < y < y_end


def create_window(win_name, win_size, win_loc):
    # creates a window to display an image
    cv2.namedWindow(win_name, flags=cv2.WINDOW_KEEPRATIO)
    win_x, win_y = win_loc
    cv2.moveWindow(win_name, win_x, win_y)
    win_width, win_height = win_size
    cv2.resizeWindow(win_name, win_width, win_height)


def show_grayscale_img(image):
    # edits an image into grayscale channel
    gray_fig = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    create_window("gray_fig", WIN_SIZE, WIN_LOC2)
    cv2.imshow("gray_fig", gray_fig)
    return gray_fig


def show_diff_img(image, background):
    # subtracts a background from an image
    diff = cv2.subtract(image, background)
    create_window("image difference", WIN_SIZE, WIN_LOC3)
    cv2.imshow("image difference", diff)
    return diff


def show_threshed_img(diff, thresh=THRESH):
    # edits an image with thresholding
    ret_val, diff = cv2.threshold(diff, thresh, 255, cv2.THRESH_BINARY)
    create_window("threshed", WIN_SIZE, WIN_LOC4)
    cv2.imshow("threshed", diff)
    return diff


def eliminate_noise(diff, it_open=1, it_close=1):
    # dilates and erodes an image to close holes and eliminate noise
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, kernel, iterations=it_close)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=it_open)
    create_window("no noise", WIN_SIZE, WIN_LOC6)
    cv2.imshow("no noise", opening)
    fruit_locs = cv2.findNonZero(opening)
    return opening, fruit_locs


def add_contours(image, initial_image, opening):
    # adds the edges of objects to an image and the rectangles that contain them to the origin
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    centers = []
    if contours is not None:
        for i, contour in enumerate(contours):
            min_max_vals = find_min_max_vals(contour)
            if min_max_vals is not None:
                min_x, min_y, max_x, max_y = min_max_vals
                # cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 0, 255))
                contoured = cv2.drawContours(image, [contour], 0, (0, 0, 255))
                create_window("contoured", WIN_SIZE, WIN_LOC5)
                cv2.imshow("contoured", contoured)
                centers.append([[(min_x + max_x) / 2, (min_y + max_y) / 2], i])
    return contours, centers


def get_text_loc(fruit, center):
    # calculates the bottom left corner of the text
    text_width, text_height = cv2.getTextSize(fruit, FONT, FONT_SCALE, THICKNESS)[0]
    text_loc = (int(center[0] - text_width / 2), int(center[1] + text_height / 2))
    return text_loc


def add_fruit_type(image, initial_image, contours, non_zero_area, centers):
    # finds the most matching fruit type and writes the type for each contour on the image
    for i, boundary in enumerate(contours):
        avg_color = average_color_finder(non_zero_area, initial_image, boundary)
        print(avg_color)
        fruit = find_similar_fruit(avg_color, FRUIT_COLORS)
        text_loc = (0, 0)
        for center in centers:
            if center[1] == i:
                text_loc = get_text_loc(fruit, center[0])
        cv2.putText(image, fruit, text_loc, FONT, FONT_SCALE, FONT_COLOR, THICKNESS)


def find_similar_fruit(avg_color, fruit_list):
    # finds which fruit in a list is the most similar to the one found
    min_diff = COLOR_SIMILARITY
    cur_fruit = '*'
    for fruit in fruit_list:
        cur_diff = find_color_difference(avg_color, fruit[0])
        if cur_diff < min_diff:
            min_diff = cur_diff
            cur_fruit = fruit[1]
    return cur_fruit


def find_color_difference(color_1, color_2):
    # finds the absolute difference between 2 colors
    arr_1 = np.array(color_1)
    arr_2 = np.array(color_2)
    diff = sum(abs(arr_1 - arr_2))
    return diff


def show_final_image(image, delay):
    # shows an image after all editing
    update = image
    create_window("edited", WIN_SIZE, WIN_LOC1)
    cv2.imshow("edited", update)
    return update


find_fruit(IMAGE, BLANK_IMAGE_GRAY)
