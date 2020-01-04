import cv2

FPS = 29
FILE_TYPE = '.mp4'
WIN_LOC = [100, 100]
WIN_RAT = 16 / 9
WIN_HEIGHT = 500
WIN_WIDTH = int(WIN_HEIGHT * WIN_RAT)
WIN_SIZE = WIN_WIDTH, WIN_HEIGHT
BLANK_IMAGE = cv2.imread('Blank_Image.png')


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
    frame_counter = 0
    while video.isOpened():
        ret_val, frame = video.read()
        if ret_val:
            frame_counter += 1
            time = calc_time(frame_counter)
            win_name = f"Frame #{frame_counter}  Time Passed:{time} s"
            create_window(win_name, WIN_SIZE, WIN_LOC)
            cv2.imshow(win_name, frame)
            k = cv2.waitKey(delay) & 0xFF
            if k == ord('s'):
                cv2.imwrite('Blank_Image.png', frame)
            if k == 27:
                cv2.destroyAllWindows()
                break
            if frame_counter == 200:
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
        else:
            break


def calc_time(frames):
    return frames / FPS


def create_window(win_name, win_size, win_loc):
    cv2.namedWindow(win_name, flags=cv2.WINDOW_KEEPRATIO)
    win_x, win_y = win_loc
    cv2.moveWindow(win_name, win_x, win_y)
    win_width, win_height = win_size
    cv2.resizeWindow(win_name, win_width, win_height)


if __name__ == "__main__":
    load_vid(delay=0)
