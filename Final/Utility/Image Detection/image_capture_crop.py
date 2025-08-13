import cv2
import numpy as np

# Global list to store clicked points
points = []

def mouse_callback(event, x, y, flags, param):
    global points, img_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        # Draw a small circle where clicked
        cv2.circle(img_copy, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Mark Corners", img_copy)

# Step 1: Capture image from USB camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not read frame.")
    exit()

# Step 2: Let user mark 4 corners
img_copy = frame.copy()
cv2.imshow("Mark Corners", img_copy)
cv2.setMouseCallback("Mark Corners", mouse_callback)

print("Click 4 corners in order (top-left, top-right, bottom-right, bottom-left) and press any key.")

cv2.waitKey(0)
cv2.destroyAllWindows()

if len(points) != 4:
    print("Error: You must click exactly 4 corners.")
    exit()

# Step 3: Crop according to selected points using perspective transform
pts1 = np.float32(points)
width = int(np.linalg.norm(np.array(points[0]) - np.array(points[1])))
height = int(np.linalg.norm(np.array(points[0]) - np.array(points[3])))
pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
cropped = cv2.warpPerspective(frame, matrix, (width, height))

# Step 4: Save cropped image
cv2.imwrite("C:\\Users\\Dell\\Desktop\\Projects\\Size_Detect_OpenCV\\Final\\Utility\\Image Detection\\cropped_image1.jpg", cropped)
print("Cropped image saved as cropped_image.jpg")

# Optional: Show cropped result
cv2.imshow("Cropped", cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
