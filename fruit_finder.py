import cv2
import numpy as np

WIN_LOC = [1000, 100]
WIN_RAT = 16 / 9
WIN_HEIGHT = 144
WIN_WIDTH = int(WIN_HEIGHT * WIN_RAT)
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT
BLANK_IMAGE = cv2.imread('Blank_Image.png')
cv2.imshow("TEST", BLANK_IMAGE)
BLANK_IMAGE_GRAY = cv2.cvtColor(BLANK_IMAGE, cv2.COLOR_BGR2GRAY)
BANNED_AREA = [[[-1, -1], [256, 17]], [[-1, 144], [20, 133]], [[256, 144], [180, 10]]]
THRESH = 50
IMAGE = cv2.imread('WATERMELON.png')


def find_fruit(image, background):
    gray_fig = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    diff = cv2.subtract(gray_fig, background)
    ret_val, diff = cv2.threshold(diff, THRESH, 255, cv2.THRESH_BINARY)
    locs = cv2.findNonZero(diff)
    if locs is not None:
        min_max_vals = find_min_max_vals(locs)
        if min_max_vals is not None:
            min_x, min_y, max_x, max_y = min_max_vals
            update = cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 0, 255))
        else:
            update = image
    else:
        update = image
    return update


def find_min_max_vals(list_3d):
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
    for rect in BANNED_AREA:
        if check_in_rectangle(rect[0], rect[1], x, y):
            return True
    return False


def check_in_rectangle(rect_start, rect_end, x, y):
    x_start = min(rect_start[0], rect_end[0])
    x_end = max(rect_start[0], rect_end[0])
    y_start = min(rect_start[1], rect_end[1])
    y_end = max(rect_start[1], rect_end[1])
    return x_start < x < x_end and y_start < y < y_end


def create_window(win_name, win_size, win_loc):
    cv2.namedWindow(win_name, flags=cv2.WINDOW_KEEPRATIO)
    win_x, win_y = win_loc
    cv2.moveWindow(win_name, win_x, win_y)
    win_width, win_height = win_size
    cv2.resizeWindow(win_name, win_width, win_height)


find_fruit(IMAGE, BLANK_IMAGE_GRAY)
