// pingtest — minimal W5500 bring-up sketch for the DT-670 readout project.
// Configures a static IP so the PC (via USB-Ethernet dongle) can ping the
// Arduino. The W5500's hardware TCP/IP stack answers ICMP echo on its own
// once the IP is set; no further code is needed for ping.
//
// PC side: set the dongle adapter to static IP 192.168.2.1, mask 255.255.255.0,
// then: ping 192.168.2.2

#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0x67, 0x00 };
IPAddress ip(192, 168, 2, 2);

void setup() {
  Serial.begin(115200);
  Ethernet.init(10);  // W5500 CS pin on Ethernet Shield 2
  Ethernet.begin(mac, ip);

  Serial.println(F("pingtest up"));
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println(F("ERROR: no W5500 detected (SPI problem?)"));
  } else {
    Serial.print(F("W5500 OK, IP: "));
    Serial.println(Ethernet.localIP());
  }
}

void loop() {
  static EthernetLinkStatus last = Unknown;
  EthernetLinkStatus now = Ethernet.linkStatus();
  if (now != last) {
    last = now;
    Serial.print(F("link: "));
    Serial.println(now == LinkON ? F("ON") : F("OFF"));
  }
  delay(500);
}
