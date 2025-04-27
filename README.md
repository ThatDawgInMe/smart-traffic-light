# smart-traffic-light

PROJECT BACKGROUND:

This Smart Traffic Light takes advantage of the integration of a Raspberry Pi 4 and an Arduino UNO R3 microcontroller to run an object detection script with Smart Zones to accurately detect if there is motion detected in a standard pedestrian cross walk. 

If there is motion detected, the Raspberry Pi sends a signal over serial communication to the Arduino to display either "WALK" or "DON'T WALK" to inform pedestrians if it is safe to cross the street. Alongside this, there is also an actual Traffic Light module that lights up in either a RED, YELLOW, or GREEN to inform pedestrians if it is safe to cross the street. 

COMPONENTS:

Raspberry Pi 4b 4GB
Arduino UNO R3
2.0" TFT LCD
Traffic Light Module
Buzzer

WIRING:

TFT LCD to Arduino UNO R3:
CS (Chip Select) --> Digital Pin 10
DC (Data/Command) --> Digital Pin 9
RST (Reset) --> Digital Pin 8
SDA (SPI Data) --> Digital Pin 11
SCL (SPI Clock) --> Digital Pin 13
VCC --> 3.3 V
GND --> GND

Traffic Light Module to Arduino UNO R3:
GND --> GND
R (Red) --> Digital Pin 2
Y (Yellow) --> Digital Pin 3
G (Green) --> Digital Pin 4

Buzzer to Arduino UNO R3:
GND --> GND
VCC --> 3.3 V

Arduino UNO R3 to Raspberry Pi 4b: SERIAL Communication (SPI) via USB 2.0 port

Arduino Sketch: smart-traffic-light/TFTDisplayWithTone/TFTDisplayWithTone.ino
Python Script: smart-traffic-light/rpi-object-detection/src/smart-traffic-light/smart-traffic-light-MAIN.py
