# New button_listener.py with I2C LCD Support

import serial
import subprocess
import time
from RPLCD.i2c import CharLCD

# Serial settings
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# I2C LCD settings
LCD_I2C_ADDRESS = 0x27  # Adjust if your LCD uses a different address
lcd = CharLCD('PCF8574', LCD_I2C_ADDRESS)

# Setup Serial communication
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Allow Arduino to reset

print("[Pi] Listening for Arduino start signal...")
lcd.clear()
lcd.write_string("Waiting for\nButton Press")

try:
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode().strip()
            print(f"[Pi] Received: {line}")

            if line == "start":
                print("[Pi] Launching cv_motion_detection.py!")
                lcd.clear()
                lcd.write_string("Launching Motion\nDetection...")
                time.sleep(1)

                subprocess.Popen(["python3", "/home/agik/Documents/GitHub/smart-traffic-light/rpi-object-detection/src/smart-traffic-light/smart-traffic-light-MAIN.py"])
                lcd.clear()
                lcd.write_string("Motion Detection\nRunning!")

except KeyboardInterrupt:
    print("[Pi] KeyboardInterrupt detected. Cleaning up...")
    arduino.close()
    lcd.clear()
    lcd.write_string("Shutdown")
