#Update 4-28-2025 11:37 PM

#!/usr/bin/python3

# Smart Motion Detection + Traffic Light Controller
import os
import sys
import cv2
import time
import numpy as np
import serial

# Import Raspberry Pi camera utilities if using PiCam
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.picamera_utils import is_raspberry_camera, get_picamera

# Settings
CAMERA_DEVICE_ID = 0
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
MOTION_THRESHOLD = 100  # Sensitivity for motion detection
IMAGE_WIDTH = 320
IMAGE_HEIGHT = 240
MOTION_BLUR = True
SMART_ZONES = [
#    (60, 80, 100, 100),
#    (180, 50, 60, 120)
    (200, 200, 80, 100)
]
BEHAVIOR_MODE = "continuous"  # "single" or "continuous"

# Setup serial communication
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Allow Arduino to reset

# Setup camera
IS_RASPI_CAMERA = is_raspberry_camera()
print("Using Raspberry Pi Camera:", IS_RASPI_CAMERA)

if IS_RASPI_CAMERA:
    cap = get_picamera(IMAGE_WIDTH, IMAGE_HEIGHT)
    cap.start()
else:
    cap = cv2.VideoCapture(CAMERA_DEVICE_ID)
    cap.set(3, IMAGE_WIDTH)
    cap.set(4, IMAGE_HEIGHT)

cnt_frame = 0
fps = 0
previous_gray = None
motion_detected = False

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def extract_zone(image, zone):
    x, y, w, h = zone
    return image[y:y+h, x:x+w]

def visualize_fps(image, fps: int):
    text_color = (0, 255, 0) if len(np.shape(image)) == 3 else (255, 255, 255)
    row_size = 20
    left_margin = 24
    fps_text = 'FPS = {:.1f}'.format(fps)
    cv2.putText(image, fps_text, (left_margin, row_size), cv2.FONT_HERSHEY_PLAIN, 1, text_color, 1)
    return image

def send_walk_cycle():
    print("[Pi] Sending WALK cycle to Arduino")
    arduino.write(b'walk\n')
    time.sleep(10)  # Walk phase
    arduino.write(b'warn\n')
    time.sleep(5)   # Warn phase
    arduino.write(b'dontwalk\n')

try:
    while True:
        start_time = time.time()

        if IS_RASPI_CAMERA:
            frame_raw = cap.capture_array()
        else:
            ret, frame_raw = cap.read()
            if not ret:
                continue

        if MOTION_BLUR:
            frame = cv2.GaussianBlur(frame_raw, (3, 3), 0)
        else:
            frame = frame_raw

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if previous_gray is not None:
            motion_found = False
            for zone in SMART_ZONES:
                zone_now = extract_zone(frame_gray, zone)
                zone_prev = extract_zone(previous_gray, zone)
                error = mse(zone_now, zone_prev)
                if error > MOTION_THRESHOLD:
                    motion_found = True
                    break  # Stop checking other zones if any motion is found

            if motion_found:
                print(f"[Pi] Motion Detected in Zones")
                if BEHAVIOR_MODE == "single":
                    if not motion_detected:
                        send_walk_cycle()
                        motion_detected = True
                elif BEHAVIOR_MODE == "continuous":
                    send_walk_cycle()
            else:
                motion_detected = False  # Reset flag when no motion

        # Draw zones
        for zone in SMART_ZONES:
            x, y, w, h = zone
            cv2.rectangle(frame_raw, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Show image
        cv2.imshow('Smart Traffic Camera', visualize_fps(frame_raw, fps))

        end_time = time.time()
        seconds = end_time - start_time
        fps = 1.0 / seconds
        cnt_frame += 1
        previous_gray = frame_gray.copy()

        if cv2.waitKey(1) == 27:  # ESC to quit
            break

except Exception as e:
    print("[Pi] Error:", e)

finally:
    print("[Pi] Exiting cleanly...")
    cv2.destroyAllWindows()
    if IS_RASPI_CAMERA:
        cap.close()
    else:
        cap.release()
    arduino.close()
