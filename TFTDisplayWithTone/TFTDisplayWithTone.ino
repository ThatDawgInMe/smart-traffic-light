#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>

// Pins
#define TFT_CS     10
#define TFT_RST    8
#define TFT_DC     9
#define BUZZER_PIN 7

Adafruit_ST7789 tft = Adafruit_ST7789(TFT_CS, TFT_DC, TFT_RST);

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);

  tft.init(240, 320);
  tft.setRotation(0);
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextSize(5);
  tft.setTextColor(ST77XX_WHITE);
}

void loop() {
  showWalk(10);         // Show WALK for 10s
  showDontWalk(20, 5);  // Show DON'T WALK for 20s, blink last 5s
}

void showWalk(int duration) {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_RED);
  tft.setCursor(60, 140);
  tft.print("STOP");

  // Optional sound
  tone(BUZZER_PIN, 880, 200);  // Beep at start
  delay(300);

  delay(duration * 1000);
}

void showDontWalk(int duration, int blinkLastSeconds) {
  int steadyTime = duration - blinkLastSeconds;

  // Steady DON'T WALK
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_GREEN);
  tft.setCursor(60, 140);
  tft.print("WALK");
  delay(steadyTime * 1000);

  // Blinking DON'T WALK
  for (int i = 0; i < blinkLastSeconds * 2; i++) {
    tft.fillScreen(i % 2 == 0 ? ST77XX_BLACK : ST77XX_YELLOW);
    if (i % 2 != 0) {
      tft.setTextColor(ST77XX_BLACK);
      tft.setCursor(60, 144);
      tft.print("HURRY");
    }
    tone(BUZZER_PIN, 1000, 150);  // Optional beep with blink
    delay(500);
  }
}
