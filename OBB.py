#Oriented Bounding Box(OBB)
import cv2
import numpy as np

# Pixels to cm ratio (adjust this based on your calibration)
ratio = 16.5 / 254  # For example, 123 pixels = 8 cm

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Thresholding (you can also try cv2.Canny for edges)
    #_, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    #edge detection
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # Skip small noisy contours
        if cv2.contourArea(cnt) < 1000:
            continue

        # Get the OBB
        rect = cv2.minAreaRect(cnt)  # ((cx, cy), (w, h), angle)
        (cx, cy), (w, h), angle = rect

        # Convert to box points
        box = cv2.boxPoints(rect)
        box = box.astype(np.intp)

        # Draw the OBB
        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

        # Convert w, h from pixels to cm
        width_cm = w * ratio
        height_cm = h * ratio

        # Display size on the image
        cv2.putText(frame, f"{width_cm:.1f}cm x {height_cm:.1f}cm", 
                    (int(cx - w/2), int(cy - h/2 - 10)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("OBB Size Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
