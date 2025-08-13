import cv2
import numpy as np
import json

# Load corners from calibration
with open("C:\\Users\\Dell\\Desktop\\Projects\\Size_Detect_OpenCV\\Final\\Utility\\VirtualGrid\\grid_corners.json", "r") as f:
    corners = json.load(f)
pts_src = np.array(corners, dtype="float32")

grid_w, grid_h = 700, 500  # set to your grid size

pts_dst = np.array([
    [0, grid_h],      # bottom-left
    [grid_w, grid_h], # bottom-right
    [grid_w, 0],      # top-right
    [0, 0]            # top-left
], dtype="float32")

matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

cap = cv2.VideoCapture(0)
print("Press SPACE to capture, Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret: break
    display = frame.copy()
    # Optionally draw the grid corners for preview
    for pt in pts_src:
        cv2.circle(display, tuple(int(v) for v in pt), 5, (0,0,255), -1)
    cv2.imshow("Webcam - Preview", display)
    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):  # SPACE to capture
        break
    elif key == ord('q'):  # Q to quit
        cap.release()
        cv2.destroyAllWindows()
        exit()

cap.release()
cv2.destroyAllWindows()

# Crop and rectify the grid area only
cropped_grid = cv2.warpPerspective(frame, matrix, (grid_w, grid_h))
cv2.imshow("Cropped Grid Area", cropped_grid)
cv2.waitKey(500)  # Show for half a second

# Preprocessing for object detection inside cropped area
gray = cv2.cvtColor(cropped_grid, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours in the cropped grid area
for cnt in contours:
    if cv2.contourArea(cnt) < 300: continue  # Filter small contours
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = box.astype(int)
    cv2.drawContours(cropped_grid, [box], 0, (0,255,0), 2)

cv2.imshow("Detected Objects in Grid Area", cropped_grid)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Optional: Save the result
cv2.imwrite("cropped_grid_detected.png", cropped_grid)
print("Detection result saved as cropped_grid_detected.png")