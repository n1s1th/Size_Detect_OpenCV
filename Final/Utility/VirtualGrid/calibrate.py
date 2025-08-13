import cv2
import numpy as np

# Helper for mouse clicks
clicked_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append([x, y])

cap = cv2.VideoCapture(2)
cv2.namedWindow("Align Grid")
cv2.setMouseCallback("Align Grid", mouse_callback)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    temp_frame = frame.copy()
    # Draw points as selected
    for pt in clicked_points:
        cv2.circle(temp_frame, tuple(pt), 5, (0,0,255), -1)

    cv2.imshow("Align Grid", temp_frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or len(clicked_points) == 4:
        break

cap.release()
cv2.destroyAllWindows()

if len(clicked_points) == 4:
    pts_src = np.array(clicked_points, dtype="float32")
    # Size of your physical grid (e.g., 400x400 px)
    grid_w, grid_h = 400, 400
    pts_dst = np.array([[0,0], [grid_w,0], [grid_w,grid_h], [0,grid_h]], dtype="float32")

    matrix = cv2.getPerspectiveTransform(pts_dst, pts_src)

    # Draw virtual grid aligned to the physical grid
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Draw grid lines in virtual space, then transform to image
        num_cells = 4
        for i in range(num_cells+1):
            # Vertical lines
            pt1 = np.array([[i*grid_w//num_cells, 0]], dtype="float32")
            pt2 = np.array([[i*grid_w//num_cells, grid_h]], dtype="float32")
            pt1_trans = cv2.perspectiveTransform(pt1[None], matrix)[0][0]
            pt2_trans = cv2.perspectiveTransform(pt2[None], matrix)[0][0]
            cv2.line(frame, tuple(pt1_trans.astype(int)), tuple(pt2_trans.astype(int)), (0,255,0), 2)
            # Horizontal lines
            pt3 = np.array([[0, i*grid_h//num_cells]], dtype="float32")
            pt4 = np.array([[grid_w, i*grid_h//num_cells]], dtype="float32")
            pt3_trans = cv2.perspectiveTransform(pt3[None], matrix)[0][0]
            pt4_trans = cv2.perspectiveTransform(pt4[None], matrix)[0][0]
            cv2.line(frame, tuple(pt3_trans.astype(int)), tuple(pt4_trans.astype(int)), (0,255,0), 2)

        cv2.imshow("Aligned Grid", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
else:
    print("Please select four corners of the grid in the image.")
