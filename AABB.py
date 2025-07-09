#Axis-Aligned Bounding Boxes (AABB)

import cv2
import numpy as np

# Pixels to cm ratio (example: 123 pixels = 8 cm)
ratio = 8 / 123

cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale and apply blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to get binary image
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Filter out small contours
        if cv2.contourArea(cnt) < 1000:
            continue

        # Get AABB (Axis-Aligned Bounding Box)
        x, y, w, h = cv2.boundingRect(cnt)

        # Draw rectangle on frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert from pixels to cm
        width_cm = w * ratio
        height_cm = h * ratio

        # Display the size
        cv2.putText(frame, f"{width_cm:.1f}cm x {height_cm:.1f}cm", 
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("AABB Size Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
