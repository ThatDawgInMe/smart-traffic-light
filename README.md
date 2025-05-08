# smart-traffic-light

## 📜 PROJECT BACKGROUND:

This Smart Traffic Light project integrates a **Raspberry Pi 4** and an **Arduino UNO R3** to create a smart pedestrian crossing system.

- The Raspberry Pi 4 runs a **smart object detection script** with **Smart Zones** to detect motion.
- If motion is detected (pedestrian presence), the Pi sends a **serial command** to the Arduino.
- The Arduino updates a **TFT LCD** to display "WALK" or "DON'T WALK" and controls a **traffic light module** (Red/Yellow/Green LEDs) and a **buzzer**.

This system simulates real-world pedestrian signals with enhanced safety checks.

---

## 🧩 COMPONENTS:

- Raspberry Pi 4B (4GB)
- Arduino UNO R3
- 2.0" 240x320 TFT LCD (SPI)
- Traffic Light Module (Red, Yellow, Green LEDs)
- Buzzer
- I2C 16x2 LCD (for Raspberry Pi status display)
- Pi Camera or USB Camera
- Breadboard, Jumper Wires

---

## 🛠 WIRING:

### TFT LCD to Arduino UNO R3:
- CS (Chip Select) --> Digital Pin 10
- DC (Data/Command) --> Digital Pin 9
- RST (Reset) --> Digital Pin 8
- SDA (SPI Data) --> Digital Pin 11
- SCL (SPI Clock) --> Digital Pin 13
- VCC --> 3.3V
- GND --> GND

### Traffic Light Module to Arduino UNO R3:
- GND --> GND
- R (Red) --> Digital Pin 2
- Y (Yellow) --> Digital Pin 3
- G (Green) --> Digital Pin 4

### Buzzer to Arduino UNO R3:
- GND --> GND
- VCC --> Digital Pin 5

### I2C LCD to Arduino UNO R3:
- VCC --> 5V
- GND --> GND
- SDA --> SDA
- SCL --> SCL

### Arduino UNO R3 to Raspberry Pi 4B:
- SERIAL Communication via USB 2.0 port

✅ Arduino GND and Raspberry Pi GND are **shared**.
✅ Recommended 330Ω resistors for LEDs.

---

## 🖥 SOFTWARE:

### Arduino Sketch:
- Path: `smart-traffic-light/TFTDisplayWithTone/TFTDisplayWithTone.ino`
- Tasks:
  - Display "DON'T WALK" at startup
  - Light up RED LED at startup
  - Send "start" when button is pressed
  - React to "walk", "warn", "dontwalk" commands from Raspberry Pi

### Raspberry Pi Python Scripts:
- `button_listener.py`
  - Listens for "start" from Arduino
  - Displays status messages on I2C LCD
  - Launches motion detection script

- `smart-traffic-light-MAIN.py`
  - Runs object detection with Smart Zones
  - Sends "walk", "warn", "dontwalk" to Arduino based on detected motion

---

## 🚦 SYSTEM FLOW:

1. **Startup**
    - Arduino powers up
    - Red LED ON
    - TFT shows "DON'T WALK"
    - Pi shows "Waiting for Button" on I2C LCD

2. **Button Pressed**
    - Arduino sends "start" over Serial
    - Raspberry Pi launches object detection
    - Pi re-confirms "DON'T WALK" and Red light

3. **Motion Detection**
    - Pi detects motion in Smart Zone
    - Pi sends "walk" → Arduino shows "WALK" (Green light)
    - After 10s, Pi sends "warn" → Arduino shows "CAUTION" (Yellow light + buzzer)
    - After 5s, Pi sends "dontwalk" → Arduino shows "DON'T WALK" (Red light)

✅ Real-world pedestrian crossing simulation!

---

## 🧠 PRE-TEST CHECKLIST:

- [ ] Arduino uploaded with Final Sketch
- [ ] Pi's `button_listener.py` and `smart-traffic-light-MAIN.py` ready
- [ ] Serial Port set correctly (`/dev/ttyACM0`)
- [ ] Camera working
- [ ] LEDs light up properly
- [ ] Buzzer beeps during warning

---
