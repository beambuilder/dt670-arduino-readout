// adsdiag — pin-level diagnostic for the ADS1115 frontend.
// Prints all four single-ended channels (vs GND) plus the A0−A1 differential
// once per second. Used to localize why the differential reads ~0 V while the
// diode itself shows 0.40 V on a multimeter: single-ended values reveal which
// input actually carries the diode potential.

#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;

void setup() {
  Serial.begin(115200);
  if (!ads.begin(0x48)) {
    Serial.println(F("ERROR: ADS1115 not found at 0x48"));
    while (true) delay(1000);
  }
  ads.setGain(GAIN_TWO);  // ±2.048 V, 62.5 uV/LSB
  Serial.println(F("adsdiag up: A0..A3 single-ended vs GND, then diff A0-A1"));
}

float readSE(uint8_t ch) {
  long sum = 0;
  for (uint8_t i = 0; i < 8; i++) sum += ads.readADC_SingleEnded(ch);
  return (sum / 8.0f) * 0.0000625f;
}

void loop() {
  float a0 = readSE(0), a1 = readSE(1), a2 = readSE(2), a3 = readSE(3);
  long sum = 0;
  for (uint8_t i = 0; i < 8; i++) sum += ads.readADC_Differential_0_1();
  float d01 = (sum / 8.0f) * 0.0000625f;

  Serial.print(F("A0="));  Serial.print(a0, 4);
  Serial.print(F("  A1=")); Serial.print(a1, 4);
  Serial.print(F("  A2=")); Serial.print(a2, 4);
  Serial.print(F("  A3=")); Serial.print(a3, 4);
  Serial.print(F("  diff01=")); Serial.print(d01, 4);
  Serial.println(F("  [V]"));
  delay(1000);
}
