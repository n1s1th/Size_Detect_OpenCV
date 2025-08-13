import cv2
import numpy as np

# ==== Detection parameters (can be adjusted) ====
MIN_AREA = 900       # Minimum contour area
MAX_AREA = 90000     # Maximum contour area
MIN_ASPECTRATIO = 1/5
MAX_ASPECTRATIO = 5
OTSU_SENSITIVITY = 22

def capture_image(cam_index=0, window_name="Capture (SPACE to save, ESC to exit)"):
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    img = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)
        if key == 27:   # ESC
            break
        elif key == 32:  # SPACE
            img = frame.copy()
            print("Image captured.")
            break
    cap.release()
    cv2.destroyAllWindows()
    return img

def calculate_difference_otsu(img, bg_img):
    bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    diff_gray = cv2.absdiff(bg_gray, img_gray)
    diff_blur = cv2.GaussianBlur(diff_gray, (5,5), 0)
    ret, otsu_thresh = cv2.threshold(diff_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if ret < OTSU_SENSITIVITY:
        diff = np.zeros_like(diff_blur)
    else:
        diff = cv2.GaussianBlur(otsu_thresh, (5,5), 0)
    return diff

def identify_valid_contours(contours, height, width):
    valid_indices = []
    for idx, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        edge_noise = x == 0 or y == 0 or (x + w) == width or (y + h) == height
        if MIN_AREA < area < MAX_AREA and MIN_ASPECTRATIO <= aspect_ratio <= MAX_ASPECTRATIO and not edge_noise:
            valid_indices.append(idx)
    return valid_indices

def detect_objects(img, bg_img):
    diff = calculate_difference_otsu(img, bg_img)
    contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    height, width = img.shape[:2]
    valid_indices = identify_valid_contours(contours, height, width)
    return contours, valid_indices

def draw_detections(img, contours, valid_indices):
    output = img.copy()
    points = []
    for i in valid_indices:
        cnt = contours[i]
        x, y, w, h = cv2.boundingRect(cnt)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00']) if M['m00'] != 0 else x + w//2
        cy = int(M['m01']/M['m00']) if M['m00'] != 0 else y + h//2
        cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(output, (cx, cy), 3, (0, 255, 0), -1)
        cv2.putText(output, f"Object {i}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
        points.append((x, y, w, h, cx, cy))
    return output, points

def main():
    print("Step 1: Capture background image (no object).")
    bg_img = capture_image(window_name="Background Image")
    if bg_img is None:
        print("Background image not captured.")
        return

    print("Step 2: Place object and capture target image.")
    img = capture_image(window_name="Target Image")
    if img is None:
        print("Target image not captured.")
        return

    print("Detecting objects...")
    contours, valid_indices = detect_objects(img, bg_img)
    output_img, detected_points = draw_detections(img, contours, valid_indices)
    print(f"Detected {len(detected_points)} object(s).")
    for idx, pt in enumerate(detected_points):
        print(f"Object {idx}: x={pt[0]}, y={pt[1]}, w={pt[2]}, h={pt[3]}, cx={pt[4]}, cy={pt[5]}")

    cv2.imshow("Detections", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("detection_result.jpg", output_img)
    print("Detection result saved as detection_result.jpg")

if __name__ == "__main__":
    main()