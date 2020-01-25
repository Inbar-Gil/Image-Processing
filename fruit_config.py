from average_color_finder import *
from fruit_finder import *

edited, contours, places = find_fruit(IMAGE, BLANK_IMAGE_GRAY)
cv2.imshow("testing", edited)
cv2.waitKey(0)

for place in places:
    # finds and displays all fruit's colors in an image
    min_x, min_y, max_x, max_y = find_min_max_vals(place)
    print(min_x)
    cv2.imshow("FOUND", edited[min_y : max_y, min_x:max_x])
    cv2.waitKey(0)
    cv2.destroyWindow("FOUND")
    print(average_color_finder(contours, IMAGE, place))
