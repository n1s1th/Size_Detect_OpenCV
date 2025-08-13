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
while True:
    ret, frame = cap.read()
    if not ret: break

    # Crop and rectify the grid area only
    cropped_grid = cv2.warpPerspective(frame, matrix, (grid_w, grid_h))

    # Preprocessing for object detection inside cropped area
    gray = cv2.cvtColor(cropped_grid, cv2.COLOR_BGR2GRAY)
    # You can use adaptive threshold or other methods for better results
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours in the cropped grid area
    for cnt in contours:
        # Filter small contours if needed
        if cv2.contourArea(cnt) < 300: continue

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = box.astype(int)
        cv2.drawContours(cropped_grid, [box], 0, (0,255,0), 2)

    cv2.imshow("Cropped Grid Area", cropped_grid)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()