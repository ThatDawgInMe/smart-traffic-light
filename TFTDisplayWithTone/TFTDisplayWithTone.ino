// Final Arduino Sketch: TFT Display + Traffic Lights + Buzzer + Button Startup + Safe Red Light
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>

// TFT Pins
#define TFT_CS     10
#define TFT_RST    8
#define TFT_DC     9

// Traffic Light Pins
#define RED_PIN    2
#define YELLOW_PIN 3
#define GREEN_PIN  4

// Buzzer Pin
#define BUZZER_PIN 5

// Button Pin
#define BUTTON_PIN 6

// Create TFT object
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  Serial.begin(9600);

  // Setup TFT
  tft.init(240, 320);
  tft.setRotation(1);
  tft.fillScreen(ST77XX_BLACK);

  // Setup Traffic Light LEDs
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);

  // Setup Buzzer
  pinMode(BUZZER_PIN, OUTPUT);

  // Setup Button
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Turn ON Red Light immediately
  digitalWrite(RED_PIN, HIGH);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);

  // Initial Display: Show "DON'T WALK"
  tft.setTextColor(ST77XX_RED);
  tft.setTextSize(3);
  tft.setCursor(10, 140);
  tft.print("DON'T WALK");

  noTone(BUZZER_PIN);
}

void loop() {
  // Check if button is pressed
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("start");

    // Optional: Show "Button Pressed" after button press
    tft.fillScreen(ST77XX_BLACK);
    tft.setTextColor(ST77XX_GREEN);
    tft.setTextSize(2);
    tft.setCursor(20, 140);
    tft.print("Button Pressed!");

    delay(500); // Debounce delay
  }

  // Check for incoming commands from Pi
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "walk") {
      showWalk();
    } else if (command == "warn") {
      warnPedestrians();
    } else if (command == "dontwalk") {
      showDontWalk();
    }
  }
}

void showWalk() {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_GREEN);
  tft.setTextSize(4);
  tft.setCursor(40, 140);
  tft.print("WALK");

  digitalWrite(GREEN_PIN, HIGH);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(RED_PIN, LOW);

  noTone(BUZZER_PIN);
}

void warnPedestrians() {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_YELLOW);
  tft.setTextSize(3);
  tft.setCursor(20, 140);
  tft.print("CAUTION");

  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(YELLOW_PIN, HIGH);
  digitalWrite(RED_PIN, LOW);

  tone(BUZZER_PIN, 1000, 500); // Beep for 500ms
}

void showDontWalk() {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_RED);
  tft.setTextSize(3);
  tft.setCursor(10, 140);
  tft.print("DON'T WALK");

  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(RED_PIN, HIGH);

  noTone(BUZZER_PIN);
}

void allLightsOff() {
  digitalWrite(RED_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
}
