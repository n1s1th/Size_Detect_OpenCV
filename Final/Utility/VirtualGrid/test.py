import cv2
import numpy as np

# ... (your calibration and perspective code) ...

num_cells_x = 8  # number of columns (horizontal, labeled A, B, ...)
num_cells_y = 8  # number of rows (vertical, labeled a, b, ...)

for col in range(num_cells_x):
    for row in range(num_cells_y):
        # Compute cell label, bottom-right is (A,a)
        hor_label = chr(ord('A') + col)
        ver_label = chr(ord('a') + row)

        # Calculate bottom-right grid cell position in virtual space
        # x increases left to right, y increases bottom to top
        cell_x = grid_w - (col + 1) * grid_w // num_cells_x + grid_w // (2 * num_cells_x)
        cell_y = grid_h - (row + 1) * grid_h // num_cells_y + grid_h // (2 * num_cells_y)

        cell_pos_virtual = np.array([[cell_x, cell_y]], dtype="float32")
        cell_pos_image = cv2.perspectiveTransform(cell_pos_virtual[None], matrix)[0][0]

        label = f"({hor_label},{ver_label})"
        cv2.putText(frame, label, tuple(cell_pos_image.astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)