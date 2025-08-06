import serial
import time
import cv2
import numpy as np
import time

# Replace 'COM3' with your Arduino port (e.g., 'COM3' on Windows)
ARDUINO_PORT = 'COM3'
BAUD_RATE = 9600
SERIAL_TIMEOUT = 5  # seconds

def findTheSize():
    # ----------- CONFIGURATION -------------
    # Fixed crop area (x, y, width, height)
    CROP_X, CROP_Y, CROP_W, CROP_H = 100, 80, 400, 300  # Adjust these as needed

    # Calibration: cm per pixel (example: 8cm / 123px)
    CM_PER_PIXEL = 8.0 / 123  # <-- Update after calibration!
    # ---------------------------------------

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open USB camera. Try changing the index to 1.")
        return 0.0, 0.0

    time.sleep(1)  # Camera warm-up

    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image from USB camera.")
        cap.release()
        return 0.0, 0.0

    crop = frame[CROP_Y:CROP_Y+CROP_H, CROP_X:CROP_X+CROP_W]
    display = crop.copy()

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest = None
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area and area > 200:
            largest = cnt
            max_area = area

    width_cm = 0.0
    height_cm = 0.0
    if largest is not None:
        rect = cv2.minAreaRect(largest)
        (cx, cy), (w, h), angle = rect
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.drawContours(display, [box], 0, (0, 255, 0), 2)
        width_cm = w * CM_PER_PIXEL
        height_cm = h * CM_PER_PIXEL
        print(f"Measured object size: {width_cm:.1f}cm x {height_cm:.1f}cm")
    else:
        print("No object detected in the selected area.")
        cv2.putText(display, "No object detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    cv2.imshow("Measured Object (USB Camera)", display)
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

    return float(width_cm), float(height_cm)

    
def sortingBaseSize(width, length):
    area = width * length

    if area < 20:
        return "small"
    else:
        return "large"



def get_user_input():
    x_coordinate = input("Enter first coordinate (string): ")
    y_coordinate = input("Enter second coordinate (string): ")
    return x_coordinate, y_coordinate

def communicate_with_arduino():
    while True:
        x_coordinate, y_coordinate = get_user_input()
        try:
            with serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT) as ser:
                time.sleep(2)  # wait for Arduino to reset after serial connect

                # Send first coordinate
                ser.write((x_coordinate + '\n').encode('utf-8'))
                time.sleep(0.1)
                # Send second coordinate
                ser.write((y_coordinate + '\n').encode('utf-8'))

                # Wait for Arduino response ("done" or "fail")
                start_time = time.time()
                response = ""
                while time.time() - start_time < SERIAL_TIMEOUT:
                    if ser.in_waiting > 0:
                        response = ser.readline().decode('utf-8').strip().lower()
                        break
                if response == "done":
                    break
                elif response == "fail":
                    print("Arduino reported failure. Please try inputting again.")
                else:
                    print("No valid response from Arduino. Please retry.")

        except serial.SerialException as e:
            print(f"Serial error: {e}. Check your port and Arduino connection.")
            time.sleep(2)

    # Find the size (width, length)
    result = findTheSize()
    if isinstance(result, tuple) and len(result) == 2:
        width, length = result
    else:
        width = length = 0.0  # defaults if your function is not implemented

    # Sort the object (returns "small" or "large")
    sort_result = sortingBaseSize(width, length)
    print(f"Sorting result: {sort_result}")

    # Send sorting result to Arduino
    try:
        with serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT) as ser:
            time.sleep(2)
            ser.write((str(sort_result) + '\n').encode('utf-8'))
    except serial.SerialException as e:
        print(f"Serial error when sending sort result: {e}")

if __name__ == "__main__":
    #communicate_with_arduino()
    findTheSize() 