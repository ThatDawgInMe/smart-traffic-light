import cv2
import time
import serial
import numpy as np

# Set up serial connection
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Give Arduino time to reset

# Set up camera
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

# Motion detection parameters
MOTION_THRESHOLD = 100
motion_detected = False

# Behavior mode: "single" or "continuous"
BEHAVIOR_MODE = "single"  # Change to "continuous" if you want

previous_gray = None

def mse(imageA, imageB):
    # Mean Squared Error between two images
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def send_walk_cycle():
    print("[Pi] Sending: walk")
    arduino.write(b'walk\n')
    time.sleep(10)  # WALK time

    print("[Pi] Sending: warn")
    arduino.write(b'warn\n')
    time.sleep(5)   # WARN time

    print("[Pi] Sending: dontwalk")
    arduino.write(b'dontwalk\n')

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)

        if previous_gray is None:
            previous_gray = gray
            continue

        error = mse(gray, previous_gray)
        previous_gray = gray

        if error > MOTION_THRESHOLD:
            print(f"[Pi] Motion Detected! MSE: {error:.2f}")

            if BEHAVIOR_MODE == "single":
                if not motion_detected:
                    send_walk_cycle()
                    motion_detected = True
            elif BEHAVIOR_MODE == "continuous":
                send_walk_cycle()
        
        else:
            # No motion
            motion_detected = False

        # Display for debugging
        cv2.imshow("Camera", gray)
        if cv2.waitKey(1) == 27:  # ESC to quit
            break

except Exception as e:
    print("[Pi] Error:", e)

finally:
    cap.release()
    arduino.close()
    cv2.destroyAllWindows()