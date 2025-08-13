import cv2

cap = cv2.VideoCapture(0)  # 0 is usually the default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Webcam Output', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()