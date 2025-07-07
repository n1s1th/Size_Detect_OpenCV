import cv2

points = []
def draw_circle(event, x, y, flags, params):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_circle)
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    for pt in points:
        cv2.circle(frame, pt, 5, (25, 15, 255), -1)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)

    if key==27:
        break


cap.release()
cv2.destroyAllWindows()