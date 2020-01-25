import cv2
from fruit_finder import find_fruit
import timeit

FPS = 10
FILE_TYPE = '.mp4'
WIN_LOC = [0, 0]
WIN_RAT = 16 / 9
WIN_HEIGHT = 240
WIN_WIDTH = int(WIN_HEIGHT * WIN_RAT)
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT
BLANK_IMAGE = cv2.imread('Blank_Image.png')
BLANK_IMAGE_GRAY = cv2.cvtColor(BLANK_IMAGE, cv2.COLOR_BGR2GRAY)


def read_file(file_name):
    # checks if a video is opened
    if FILE_TYPE not in file_name:
        print(f'The file must be of type{FILE_TYPE}')
        return False
    cap_vid = cv2.VideoCapture(file_name)
    if cap_vid.isOpened():
        return cap_vid
    print(f'File named {file_name} does not exist')
    return False


def load_vid(file='', delay=0):
    # loads a video in the cv2 library
    captured_vid = read_file(file)
    while not captured_vid:
        file = input("Input File Name")
        captured_vid = read_file(file)
        if captured_vid:
            display_vid(captured_vid, delay)


def display_vid(video_in, delay):
    # this function edits the video frame by frame and rewrites it
    frame_counter = 0
    background = BLANK_IMAGE_GRAY
    prev_frame = None
    video_out = cv2.VideoWriter('Edited_fruit_ninja_Blank.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), FPS,
                                (256, 144))
    while video_in.isOpened():
        ret_val, frame = video_in.read()
        if ret_val:
            if user_input(frame_counter, delay, frame) == -1:
                break
            if user_input(frame_counter, delay, frame) == 1:
                print(frame_counter)
                continue
            background = check_for_background(frame, prev_frame, background)
            frame_counter = display_images(frame_counter, frame, background)
            video_out.write(frame)
            cv2.destroyAllWindows()
            prev_frame = frame.copy()
        else:
            break
    release_videos(video_in, video_out)


def calc_time(frames):
    return frames / FPS


def create_window(win_name, win_size, win_loc):
    # creates a window to display an image
    cv2.namedWindow(win_name, flags=cv2.WINDOW_KEEPRATIO)
    win_x, win_y = win_loc
    cv2.moveWindow(win_name, win_x, win_y)
    win_width, win_height = win_size
    cv2.resizeWindow(win_name, win_width, win_height)


def find_background(frame_1, frame_2):
    # checks whether the background of a video has changed
    gray_1 = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
    gray_2 = cv2.cvtColor(frame_2, cv2.COLOR_BGR2GRAY)
    diff = cv2.subtract(gray_1, gray_2)
    diff_locs = cv2.findNonZero(diff)
    if diff_locs is None:
        return True
    if len(diff_locs) < 20:
        return True
    return False


def check_for_background(frame, prev_frame, background):
    # manages the change of background
    if prev_frame is None:
        prev_frame = frame
    if find_background(prev_frame, frame):
        background = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    return background


def display_images(frame_counter, frame, background):
    # edits a specific image and displays the whole editing process
    time = calc_time(frame_counter)
    win_name = f"Frame #{frame_counter}  Time Passed:{time} s"
    create_window(win_name, WIN_SIZE, WIN_LOC)
    fruit_found, fruit_locs, contours = find_fruit(frame, background)
    cv2.imshow(win_name, fruit_found)
    return frame_counter + 1


def user_input(frame_counter, delay, frame):
    # checks and acts on user input
    k = cv2.waitKey(delay) & 0xFF
    # k == ord('s')
    if frame_counter == 655:
        cv2.imshow(f"{frame_counter}", frame)
        cv2.imwrite(f'LIME{frame_counter}.png', frame)
    if k == 27:
        cv2.destroyAllWindows()
        return -1
    if frame_counter == 1000:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return -1


def release_videos(video_in, video_out):
    # releases and saves both input and output videos
    video_in.release()
    video_out.release()


if __name__ == "__main__":
    load_vid(delay=1)
