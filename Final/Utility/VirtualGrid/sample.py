import cv2
import json

clicked_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append([x, y])

cap = cv2.VideoCapture(0)
cv2.namedWindow("Calibrate")
cv2.setMouseCallback("Calibrate", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret: break
    temp = frame.copy()
    for pt in clicked_points:
        cv2.circle(temp, tuple(pt), 5, (0,0,255), -1)
    cv2.imshow("Calibrate", temp)
    if cv2.waitKey(1) & 0xFF == ord('q') or len(clicked_points) == 4: break

cap.release()
cv2.destroyAllWindows()

if len(clicked_points) == 4:
    with open("grid_corners.json", "w") as f:
        json.dump(clicked_points, f)
    print("Saved grid corners:", clicked_points)
else:
    print("Calibration incomplete.")