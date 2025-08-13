import cv2

def draw_grid(img, grid_size=50, color=(0,255,0), thickness=1):
    height, width, _ = img.shape
    # Draw vertical lines
    for x in range(0, width, grid_size):
        cv2.line(img, (x, 0), (x, height), color, thickness)
    # Draw horizontal lines
    for y in range(0, height, grid_size):
        cv2.line(img, (0, y), (width, y), color, thickness)
    return img

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_with_grid = draw_grid(frame.copy(), grid_size=70)  # Change grid_size as needed

    cv2.imshow('Webcam with Grid', frame_with_grid)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()