import serial
import time

SERIAL_PORT = 'COM6'
BAUD_RATE = 9600

def send_to_arduino(ser, message):
    ser.write((message + '\n').encode())
    print(f"Sent to Arduino: {message}")

def read_from_arduino(ser, timeout=10):
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
            return response
        time.sleep(0.1)
    print("No response from Arduino (timeout).")
    return None

def main():
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
            # Prompt for both inputs (case sensitive!)
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

            # Send single line input as Arduino expects, e.g. "A c"
            send_to_arduino(ser, f"{slider_input} {robot_input}")
            read_from_arduino(ser)

            # Wait for Arduino to prompt for sorted area action
            while True:
                response = read_from_arduino(ser)
                if response and ("sorted area action" in response or "Enter sorted area action" in response):
                    break
                if response and ("Enter slider position" in response or "slider position" in response):
                    break

            # Prompt for sorted area action (case sensitive!)
            while True:
                sort_input = input("Enter sorted area action (b1, b2, b3, b4): ").strip()
                if sort_input in ['b1', 'b2', 'b3', 'b4']:
                    break
                print("Invalid input. Please enter one of: b1, b2, b3, b4 (case sensitive).")

            send_to_arduino(ser, sort_input)
            read_from_arduino(ser)

            # Wait for Arduino to prompt for next round
            while True:
                response = read_from_arduino(ser)
                if response and ("Enter slider position" in response or "slider position" in response):
                    print("Round complete! Starting next round.\n")
                    break

    except KeyboardInterrupt:
        print("Exiting program.")

    ser.close()

if __name__ == "__main__":
    main()