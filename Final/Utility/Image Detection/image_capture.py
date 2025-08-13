import cv2

# Open the first camera (0 = first detected USB or built-in camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Read a single frame
ret, frame = cap.read()

if not ret:
    print("Error: Could not read frame.")
    cap.release()
    exit()

# Save the image
cv2.imwrite("C:\\Users\\Dell\\Desktop\\Projects\\Size_Detect_OpenCV\\Final\\Utility\\Image Detection", frame)

print("Image saved as captured_image.jpg")

# Release the camera
cap.release()

# Optional: Show the image in a window
cv2.imshow("Captured Image", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
