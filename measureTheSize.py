import cv2
import math

points = []

#Pixels to cm ratio
ratio=10/162
# This ratio is based on a known measurement (e.g., 10 cm corresponds to 137 pixels).


def draw_circle(event, x, y, flags, params):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) == 2:
            points = []
        points.append((x, y))

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_circle)
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    for pt in points:
        cv2.circle(frame, pt, 5, (25, 15, 255), -1)


    #Measure the distance between two points
    if len(points) == 2:
        pt1 = points[0]
        pt2 = points[1]
        distance_px = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])


    #Distance to CM
        distance_cm = distance_px * ratio
        
        cv2.putText(frame, fr"{int(distance_cm)}cm", (pt1[0], pt1[1] - 10), cv2.FONT_HERSHEY_PLAIN, 2.5, (25, 15, 235), 2)
    

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)

    if key==27:
        break


cap.release()
cv2.destroyAllWindows()