import serial
import time

# --- Serial Setup ---
SERIAL_PORT = 'COM6'
BAUD_RATE = 9600

# --- Sorted Area Config ---
CELL_WIDTH_CM = 5
SCANNING_AREA_CM = 35
sortedAreaStartCM_map = {
    'b1': 50,
    'b2': 50,
    'b3': 60,
    'b4': 60
}
roundCount = {
    'b1': 0,
    'b2': 0,
    'b3': 0,
    'b4': 0
}

def send_to_arduino(ser, message):
    ser.write((message + '\n').encode())
    print(f"Sent to Arduino: {message}")

def read_from_arduino(ser, timeout=10):
    ser.timeout = 1
    start = time.time()
    while time.time() - start < timeout:
        if ser.in_waiting:
            response = ser.readline().decode().strip()
            print(f"Arduino: {response}")
            return response
        time.sleep(0.1)
    print("No response from Arduino (timeout).")
    return None

def move_slider_to_cell(ser, slider_input):
    cell_num = ord(slider_input) - ord('A') + 1
    cell_cm = cell_num * CELL_WIDTH_CM
    send_to_arduino(ser, f"SLIDER:{cell_cm}")

def trigger_robot_arm(ser, robot_input):
    send_to_arduino(ser, f"ROBOT:{robot_input}")

def move_slider_to_scanning_area(ser):
    send_to_arduino(ser, f"SLIDER:{SCANNING_AREA_CM}")

def trigger_scanning_actions(ser):
    send_to_arduino(ser, "SCANNINGDROP")
    send_to_arduino(ser, "SCANNINGPICK")

def sorted_area_action(ser, sort_input):
    start_cm = sortedAreaStartCM_map[sort_input]
    current_round = roundCount[sort_input]
    position_cm = start_cm + current_round * CELL_WIDTH_CM
    send_to_arduino(ser, f"SORTED:{sort_input.upper()}:{position_cm}")
    send_to_arduino(ser, f"ROBOT_SORT:{sort_input}")
    roundCount[sort_input] += 1

def home_slider(ser):
    send_to_arduino(ser, "HOME")

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Let Arduino initialize
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        return

    print("Arduino Python Control Started.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            # Prompt for both inputs
            while True:
                slider_input = input("Enter slider position (A, B, C, D): ").strip().upper()
                if slider_input in ['A', 'B', 'C', 'D']:
                    break
                print("Invalid input. Please enter one of: A, B, C, D.")

            while True:
                robot_input = input("Enter robot arm action (a, b, c, d): ").strip().lower()
                if robot_input in ['a', 'b', 'c', 'd']:
                    break
                print("Invalid input. Please enter one of: a, b, c, d.")

            # Step 1: Move slider to selected position
            move_slider_to_cell(ser, slider_input)
            read_from_arduino(ser)

            # Step 2: Trigger robot arm function
            trigger_robot_arm(ser, robot_input)
            read_from_arduino(ser)

            # Step 3: Move slider to scanning area
            move_slider_to_scanning_area(ser)
            read_from_arduino(ser)

            # Step 4: Trigger scanningdrop and scanningpick
            trigger_scanning_actions(ser)
            read_from_arduino(ser)

            # Prompt for sorted area action
            while True:
                sort_input = input("Enter sorted area action (b1, b2, b3, b4): ").strip()
                if sort_input in ['b1', 'b2', 'b3', 'b4']:
                    break
                print("Invalid input. Please enter one of: b1, b2, b3, b4.")

            sorted_area_action(ser, sort_input)
            read_from_arduino(ser)

            # After completion, return slider to home
            home_slider(ser)
            read_from_arduino(ser)

            print("Round complete! Starting next round.\n")

    except KeyboardInterrupt:
        print("Exiting program.")

    ser.close()

if __name__ == "__main__":
    main()