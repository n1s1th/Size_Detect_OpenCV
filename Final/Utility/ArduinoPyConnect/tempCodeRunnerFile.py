import serial
import time
import os

SERIAL_PORT = 'COM6'
BAUD_RATE = 9600
TRAY_FILE = "tray_counts.txt"

# Initialize tray counts
tray_counts = {"b1": 0, "b2": 0, "b3": 0, "b4": 0}

def load_tray_counts():
    if os.path.exists(TRAY_FILE):
        with open(TRAY_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(" count", "")
                    if key in tray_counts:
                        try:
                            tray_counts[key] = int(parts[1].strip())
                        except ValueError:
                            tray_counts[key] = 0

def save_tray_counts():
    with open(TRAY_FILE, "w") as f:
        for key in ["b1", "b2", "b3", "b4"]:
            f.write(f"{key.upper()} count: {tray_counts[key]}\n")

def send_to_arduino(ser, message):
    ser.write((message + '\n').encode())
    print(f"Sent to Arduino: {message}")

def read_from_arduino(ser, expected=None, timeout=15):
    ser.timeout = 1
    start = time.time()
    while time.time() - start < timeout:
        if ser.in_waiting:
            raw = ser.readline()
            try:
                response = raw.decode('utf-8').strip()
            except UnicodeDecodeError:
                response = raw.decode('utf-8', errors='replace').strip()
            print(f"Arduino: {response}")
            if expected and expected in response:
                return response
            elif not expected:
                return response
        time.sleep(0.1)
    print("No response from Arduino (timeout).")
    return None

def main():
    load_tray_counts()

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
    except Exception as e:
        print(f"Failed to open serial port: {e}")
        return

    print("Arduino Python Control Started.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            # 1. Prompt for slider and robot arm input
            while True:
                slider_input = input("Enter slider position (A, B, C, D): ").strip()
                if slider_input in ['A', 'B', 'C', 'D']:
                    break
                print("Invalid input. Please enter one of: A, B, C, D (case sensitive).")

            while True:
                robot_input = input("Enter robot arm action (a, b, c, d): ").strip()
                if robot_input in ['a', 'b', 'c', 'd']:
                    break
                print("Invalid input. Please enter one of: a, b, c, d (case sensitive).")

            # 2. Send combined input to Arduino
            send_to_arduino(ser, f"{slider_input} {robot_input}")

            # 3. Wait for Arduino to signal ready to scan
            read_from_arduino(ser, expected="READY_TO_SCAN")

            # 4. Prompt for sorted tray
            while True:
                tray_input = input("Enter sorted area tray (b1, b2, b3, b4): ").strip()
                if tray_input in ['b1', 'b2', 'b3', 'b4']:
                    break
                print("Invalid input. Please enter one of: b1, b2, b3, b4 (case sensitive).")

            # 5. Send tray number to Arduino
            send_to_arduino(ser, tray_input)

            # 6. Wait for Arduino to confirm pick/sorting
            read_from_arduino(ser, expected="ROUND_COMPLETE")

            # 7. Increment and log tray count
            tray_counts[tray_input] += 1
            save_tray_counts()
            print(f"\nTray counts so far:")
            for key in ["b1", "b2", "b3", "b4"]:
                print(f"{key.upper()} count: {tray_counts[key]}")
            print("\nStarting next round...\n")

    except KeyboardInterrupt:
        print("Exiting program.")

    ser.close()

if __name__ == "__main__":
    main()