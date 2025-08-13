import cv2
import numpy as np

# --- CONFIGURABLE PARAMETERS ---
grid_w, grid_h = 700, 500          # Virtual grid size in pixels (for perspective warping)
num_cells_x, num_cells_y = 7, 5    # Number of grid columns and rows

# --- GLOBALS FOR MOUSE CALLBACK ---
clicked_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append([x, y])

def draw_grid_and_labels(frame, matrix, grid_w, grid_h, num_cells_x, num_cells_y):
    # Draw grid lines
    # Vertical lines
    for i in range(num_cells_x + 1):
        pt1 = np.array([[i * grid_w // num_cells_x, 0]], dtype="float32")
        pt2 = np.array([[i * grid_w // num_cells_x, grid_h]], dtype="float32")
        pt1_trans = cv2.perspectiveTransform(pt1[None], matrix)[0][0]
        pt2_trans = cv2.perspectiveTransform(pt2[None], matrix)[0][0]
        cv2.line(frame, tuple(pt1_trans.astype(int)), tuple(pt2_trans.astype(int)), (0,255,0), 2)
    # Horizontal lines
    for j in range(num_cells_y + 1):
        pt3 = np.array([[0, j * grid_h // num_cells_y]], dtype="float32")
        pt4 = np.array([[grid_w, j * grid_h // num_cells_y]], dtype="float32")
        pt3_trans = cv2.perspectiveTransform(pt3[None], matrix)[0][0]
        pt4_trans = cv2.perspectiveTransform(pt4[None], matrix)[0][0]
        cv2.line(frame, tuple(pt3_trans.astype(int)), tuple(pt4_trans.astype(int)), (0,255,0), 2)

    # Draw cell labels
    for col in range(num_cells_x):
        for row in range(num_cells_y):
            hor_label = chr(ord('A') + col)
            ver_label = chr(ord('a') + row)
            # Bottom-right origin:
            cell_x = grid_w - (col + 1) * grid_w // num_cells_x + grid_w // (2 * num_cells_x)
            cell_y = grid_h - (row + 1) * grid_h // num_cells_y + grid_h // (2 * num_cells_y)
            cell_pos_virtual = np.array([[cell_x, cell_y]], dtype="float32")
            cell_pos_image = cv2.perspectiveTransform(cell_pos_virtual[None], matrix)[0][0]

            label = f"({hor_label},{ver_label})"
            cv2.putText(frame, label, tuple(cell_pos_image.astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    return frame

def main():
    print("OpenCV Grid Alignment Tool")
    print("Step 1: Select the FOUR corners of your physical grid in the camera image (ORDER: bottom-right, bottom-left, top-left, top-right or any order, just be consistent with virtual grid corners).")
    print("Step 2: Press 'q' to continue after selecting 4 points.")

    # Start webcam and collect 4 points
    cap = cv2.VideoCapture(0)
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
        # The destination (virtual grid) corners: bottom-right, bottom-left, top-left, top-right
        pts_dst = np.array([
            [grid_w, grid_h],        # bottom-right
            [0, grid_h],             # bottom-left
            [0, 0],                  # top-left
            [grid_w, 0]              # top-right
        ], dtype="float32")

        pts_src = np.array(clicked_points, dtype="float32")
        matrix = cv2.getPerspectiveTransform(pts_dst, pts_src)

        # Main display loop
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_with_grid = draw_grid_and_labels(frame.copy(), matrix, grid_w, grid_h, num_cells_x, num_cells_y)
            cv2.imshow("Virtual Grid with Labels", frame_with_grid)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Please select four corners of the grid in the image.")

if __name__ == "__main__":
    main()