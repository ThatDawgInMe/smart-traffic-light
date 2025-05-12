#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

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

// TFT Display (240x320)
Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

// I2C LCD (16x2 at address 0x27)
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);

  // Initialize TFT
  tft.init(240, 320);
  tft.setRotation(-1);
  tft.fillScreen(ST77XX_BLACK);

  // Initialize I2C LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("System Ready");
  lcd.setCursor(0, 1);
  lcd.print("Waiting for Pi");

  // Setup pins
  pinMode(RED_PIN, OUTPUT);
  pinMode(YELLOW_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Start with RED light and DON'T WALK
  digitalWrite(RED_PIN, HIGH);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);

  showDontWalk();
  noTone(BUZZER_PIN);
}

void loop() {
  // Handle serial input from Raspberry Pi
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "walk") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Pi: WALK signal");
      showWalk();
    } else if (command == "warn") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Pi: WARN signal");
      showWarn();
    } else if (command == "dontwalk") {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Pi: DONTWALK");
      showDontWalk();
    }
  }
}

void showWalk() {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_GREEN);
  tft.setTextSize(5);
  tft.setCursor(40, 140);
  tft.print("WALK");

  digitalWrite(GREEN_PIN, HIGH);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(RED_PIN, LOW);

  tone(BUZZER_PIN, 2000, 500);
}

void showWarn() {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_YELLOW);
  tft.setTextSize(4);
  tft.setCursor(20, 140);
  tft.print("CAUTION");

  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(YELLOW_PIN, HIGH);
  digitalWrite(RED_PIN, LOW);

  tone(BUZZER_PIN, 1000, 500); // Beep
}

void showDontWalk() {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_RED);
  tft.setTextSize(5);
  tft.setCursor(10, 140);
  tft.print("DON'T WALK");

  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(YELLOW_PIN, LOW);
  digitalWrite(RED_PIN, HIGH);

  noTone(BUZZER_PIN);
}
