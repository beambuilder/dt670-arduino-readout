// noisecap - stream raw ADS1115 differential samples over serial for noise analysis.
//
// ADS1115 diff A0-A1, GAIN_TWO (+/-2.048 V, 62.5 uV/LSB), 860 SPS continuous.
// Sampled every 5 ms (200 Hz) so each read is a fresh conversion and the
// 115200-baud link is not saturated. Output: CSV lines "t_us,raw".
//
// Used for the 10 uF rail-decoupling A/B comparison (2026-07-31).
// NOTE: flashing this replaces dt670srv - reflash it afterwards.

#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads;

const uint32_t SAMPLE_INTERVAL_US = 5000;  // 200 Hz

void setup() {
  Serial.begin(115200);
  ads.setGain(GAIN_TWO);
  ads.setDataRate(RATE_ADS1115_860SPS);
  if (!ads.begin()) {  // addr 0x48
    Serial.println(F("ERR ads1115 not found"));
    while (1) {}
  }
  // continuous conversions, differential A0-A1
  ads.startADCReading(ADS1X15_REG_CONFIG_MUX_DIFF_0_1, /*continuous=*/true);
  delay(10);  // first conversion
  Serial.println(F("t_us,raw"));
}

void loop() {
  static uint32_t next_us = 0;
  uint32_t now = micros();
  if ((int32_t)(now - next_us) >= 0) {
    next_us = now + SAMPLE_INTERVAL_US;
    int16_t raw = ads.getLastConversionResults();
    Serial.print(now);
    Serial.print(',');
    Serial.println(raw);
  }
}
