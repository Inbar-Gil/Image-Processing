import cv2
from fruit_finder import find_fruit
import timeit

FPS = 29
FILE_TYPE = '.mp4'
WIN_LOC = [300, 100]
WIN_RAT = 16 / 9
WIN_HEIGHT = 500
WIN_WIDTH = int(WIN_HEIGHT * WIN_RAT)
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT
BLANK_IMAGE = cv2.imread('Blank_Image.png')
BLANK_IMAGE_GRAY = cv2.cvtColor(BLANK_IMAGE, cv2.COLOR_BGR2GRAY)


def read_file(file_name):
    if FILE_TYPE not in file_name:
        print(f'The file must be of type{FILE_TYPE}')
        return False
    cap_vid = cv2.VideoCapture(file_name)
    if cap_vid.isOpened():
        return cap_vid
    print(f'File named {file_name} does not exist')
    return False


def load_vid(file='', delay=0):
    captured_vid = read_file(file)
    while not captured_vid:
        file = input("Input File Name")
        captured_vid = read_file(file)
        display_vid(captured_vid, delay)


def display_vid(video, delay):
    now = timeit.timeit()
    frame_counter = 0
    background = BLANK_IMAGE_GRAY
    prev_frame = BLANK_IMAGE
    video_out = cv2.VideoWriter('Edited_fruit_ninja.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 29, (256, 144))
    while video.isOpened():
        ret_val, frame = video.read()
        if ret_val:
            if find_background(prev_frame, frame):
                background = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            frame_counter += 1
            time = calc_time(frame_counter)
            """win_name = f"Frame #{frame_counter}  Time Passed:{time} s"
            #create_window(win_name, WIN_SIZE, WIN_LOC)"""
            fruit_found = find_fruit(frame, background)
            video_out.write(fruit_found)
            k = cv2.waitKey(delay) & 0xFF
            if k == ord('s'):
                cv2.imwrite('WATERMELON.png', frame)
            if k == 27:
                cv2.destroyAllWindows()
                break
            """if frame_counter == 200:
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break"""
            prev_frame = frame
            if time > 30:
                break
        else:
            break
    video.release()
    video_out.release()


def calc_time(frames):
    return frames / FPS


def create_window(win_name, win_size, win_loc):
    cv2.namedWindow(win_name, flags=cv2.WINDOW_KEEPRATIO)
    win_x, win_y = win_loc
    cv2.moveWindow(win_name, win_x, win_y)
    win_width, win_height = win_size
    cv2.resizeWindow(win_name, win_width, win_height)


def find_background(frame_1, frame_2):
    gray_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)
    diff = cv2.subtract(gray_1, gray_2)
    diff_locs = cv2.findNonZero(diff)
    if diff_locs is None:
        return True
    if len(diff_locs) < 20:
        return True
    return False


if __name__ == "__main__":
    load_vid(delay=1)
