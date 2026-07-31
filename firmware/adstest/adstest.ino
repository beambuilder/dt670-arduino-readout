// adstest — bench verification of the ADS1115 frontend for the DT-670 readout.
// Reads the diode voltage differentially on A0−A1 (PGA ±2.048 V, 62.5 µV/LSB),
// averages 64 samples, prints volts over serial once per second.
// Compare against a multimeter across the diode: values should agree within a few mV.

#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;

void setup() {
  Serial.begin(115200);
  if (!ads.begin(0x48)) {
    Serial.println(F("ERROR: ADS1115 not found at 0x48 (check SDA->A4, SCL->A5, VDD, GND)"));
    while (true) delay(1000);
  }
  ads.setGain(GAIN_TWO);  // ±2.048 V range
  Serial.println(F("adstest up, ADS1115 OK"));
}

void loop() {
  long sum = 0;
  for (uint8_t i = 0; i < 64; i++) {
    sum += ads.readADC_Differential_0_1();
  }
  float volts = (sum / 64.0f) * 0.0000625f;  // 62.5 uV/LSB at GAIN_TWO

  Serial.print(F("V_diode = "));
  Serial.print(volts, 5);
  Serial.print(F(" V"));
  if (volts > 1.5f) Serial.print(F("  [open sensor / rail?]"));
  if (volts < -0.05f) Serial.print(F("  [reversed polarity]"));
  Serial.println();
  delay(1000);
}
