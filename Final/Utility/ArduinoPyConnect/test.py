import serial
import time

ser = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)

# Read and print Arduino's startup messages
while True:
    if ser.in_waiting:
        print(ser.readline().decode('utf-8').strip())
        break

# Send input to Arduino
ser.write(b"B c\n")

# Print Arduino response
while True:
    if ser.in_waiting:
        print(ser.readline().decode('utf-8').strip())
        break

ser.close()