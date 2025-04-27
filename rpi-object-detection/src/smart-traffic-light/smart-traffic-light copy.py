#!/usr/bin/python3

# Modified cv_motion_detection.py with Smart Motion Zones

import os
import sys
import cv2
import time
import numpy as np
import serial
import RPi.GPIO as GPIO
from time import sleep

# Add src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.picamera_utils import is_raspberry_camera, get_picamera

CAMERA_DEVICE_ID = 0
# Set up serial to Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600)  # Adjust if needed
time.sleep(2)  # Wait for Arduino to reset

IMAGE_WIDTH = 320
IMAGE_HEIGHT = 240
IS_RASPI_CAMERA = is_raspberry_camera()
MOTION_BLUR = True

MOTION_THRESHOLD = 100  # Sensitivity for motion detection

cnt_frame = 0
fps = 0

print("Using raspi camera: ", IS_RASPI_CAMERA)

# Define Smart Motion Zones (x, y, width, height)
zones = [
    (60, 80, 100, 100),  # Example zone in the middle
    (180, 50, 60, 120)   # Another example zone
]

def mse(image_a, image_b):
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])
    return err

def visualize_fps(image, fps: int):
    if len(np.shape(image)) < 3:
        text_color = (255, 255, 255)  # white
    else:
        text_color = (0, 255, 0)  # green
    row_size = 20  # pixels
    left_margin = 24  # pixels

    font_size = 1
    font_thickness = 1

    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)
    return image

def extract_zone(image, zone):
    x, y, w, h = zone
    return image[y:y+h, x:x+w]

if __name__ == "__main__":
    try:
        if IS_RASPI_CAMERA:
            cap = get_picamera(IMAGE_WIDTH, IMAGE_HEIGHT)
            cap.start()
        else:
            cap = cv2.VideoCapture(CAMERA_DEVICE_ID)
            cap.set(3, IMAGE_WIDTH)
            cap.set(4, IMAGE_HEIGHT)

        previous_gray = None

        while True:
            start_time = time.time()

            if IS_RASPI_CAMERA:
                frame_raw = cap.capture_array()
            else:
                _, frame_raw = cap.read()

            if MOTION_BLUR:
                frame = cv2.GaussianBlur(frame_raw, (3, 3), 0)
            else:
                frame = frame_raw

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if previous_gray is not None:
                for zone in zones:
                    zone_now = extract_zone(frame_gray, zone)
                    zone_prev = extract_zone(previous_gray, zone)

                    error = mse(zone_now, zone_prev)

                    if error > MOTION_THRESHOLD:
                        print(f'Frame {cnt_frame}: Motion Detected in Zone {zone}!')
                        arduino.write(b'motion\n')

            # Draw zones for visualization
            for zone in zones:
                x, y, w, h = zone
                cv2.rectangle(frame_raw, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Show images
            cv2.imshow('Camera View', visualize_fps(frame_raw, fps))
            cv2.imshow('Gray', frame_gray)

            end_time = time.time()
            seconds = end_time - start_time
            fps = 1.0 / seconds

            cnt_frame += 1
            previous_gray = frame_gray.copy()

            if cv2.waitKey(1) == 27:
                break

    except Exception as e:
        print(e)
    finally:
        cv2.destroyAllWindows()
        cap.close() if IS_RASPI_CAMERA else cap.release()
        arduino.close()