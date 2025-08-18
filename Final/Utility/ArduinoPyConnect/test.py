import serial
import time

SERIAL_PORT = 'COM6'
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# Print Arduino startup messages
while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        print("Arduino:", line)
        if "slider position" in line:
            break

# Prompt user and send input to Arduino
user_input = input("Enter slider position and arm (e.g. C c): ")
ser.write((user_input + '\n').encode())
print("Sent:", user_input)

# Continue to read Arduino responses (for the next steps)
while True:
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()
        print("Arduino:", line)
        # Add more logic here for the rest of your workflow
        break

ser.close()