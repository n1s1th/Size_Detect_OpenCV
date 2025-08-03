from picamera2 import Picamera2
import cv2
import numpy as np
import time

# ----------- CONFIGURATION -------------
# Fixed crop area (x, y, width, height)
CROP_X, CROP_Y, CROP_W, CROP_H = 100, 80, 400, 300  # Adjust as needed

# Calibration: cm per pixel (example: 8cm / 123px)
CM_PER_PIXEL = 8.0 / 123  # <-- Update with your own calibration!

# ---------------------------------------

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "BGR888"
picam2.configure("preview")
picam2.start()

time.sleep(1)  # Camera warm-up

print("Press SPACE to capture and measure the object in the cropped area. Press ESC to exit.")

while True:
    frame = picam2.capture_array()
    # Crop the region of interest
    crop = frame[CROP_Y:CROP_Y+CROP_H, CROP_X:CROP_X+CROP_W]
    display = crop.copy()

    # Show the cropped area live for positioning
    cv2.rectangle(frame, (CROP_X, CROP_Y), (CROP_X+CROP_W, CROP_Y+CROP_H), (0,255,0), 2)
    cv2.imshow("Full Camera (crop area highlighted)", frame)
    cv2.imshow("Cropped Area", crop)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC to exit
        break
    elif key == 32:  # SPACE to capture and measure
        # Convert to grayscale, blur, and threshold for contour detection
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour in the cropped area
        largest = None
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area and area > 200:  # Filter small noise
                largest = cnt
                max_area = area

        if largest is not None:
            rect = cv2.minAreaRect(largest)
            (cx, cy), (w, h), angle = rect
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            cv2.drawContours(display, [box], 0, (0, 255, 0), 2)
            width_cm = w * CM_PER_PIXEL
            height_cm = h * CM_PER_PIXEL
            cv2.putText(display, f"{width_cm:.1f}cm x {height_cm:.1f}cm",
                        (int(cx - w/2), int(cy - h/2 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(display, "No object detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        # Show the result
        cv2.imshow("Measured Object", display)
        cv2.waitKey(0)  # Wait for any key before continuing

cv2.destroyAllWindows()