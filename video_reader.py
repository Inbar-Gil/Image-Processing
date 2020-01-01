import cv2

FPS = 29
FILE_TYPE = '.mp4'


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
        # captured_vid.release()
        # cv2.destroyAllWindows()


def display_vid(video, delay):
    frame_counter = 0
    while video.isOpened():
        ret_val, frame = video.read()
        if ret_val:
            frame_counter += 1
            time = calc_time(frame_counter)
            cv2.imshow(f"Frame #{frame_counter}  Time Passed:{time} s", frame)
            cv2.waitKey(delay)
            if frame_counter == 29:
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
        else:
            break


def calc_time(frames):
    return frames / FPS


if __name__ == "__main__":
    load_vid(delay=int(1000))

