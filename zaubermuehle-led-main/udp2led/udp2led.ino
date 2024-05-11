
#include <FastLED.h>
#include <Ethernet.h>
#include <EthernetUdp.h>

// network config
byte mac[] = {
  0x90, 0xA2, 0xDA, 0x0E, 0xF4, 0x91
};
IPAddress ip(192, 168, 11, 100);
unsigned int localPort = 3456;

#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB

#define LED_STRINGS     4
#define LEDS_PER_STRING 90

#define DATA_PIN_1    6
#define DATA_PIN_2    8
#define DATA_PIN_3    10
#define DATA_PIN_4    12

CRGB leds[LED_STRINGS][LEDS_PER_STRING];

#define OVERALL_BRIGHTNESS  10


char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
EthernetUDP Udp;


void setup() {

  // handy to have a delay on startup so if FastLED crashes we don't lock ourselves out of the arduino.
  delay(3000);

  FastLED.addLeds<LED_TYPE, DATA_PIN_1, COLOR_ORDER>(leds[0], LEDS_PER_STRING);//.setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, DATA_PIN_2, COLOR_ORDER>(leds[1], LEDS_PER_STRING);//.setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, DATA_PIN_3, COLOR_ORDER>(leds[2], LEDS_PER_STRING);//.setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, DATA_PIN_4, COLOR_ORDER>(leds[3], LEDS_PER_STRING);//.setCorrection(TypicalLEDStrip);

  FastLED.setBrightness(OVERALL_BRIGHTNESS);


  Ethernet.begin(mac, ip);
  Udp.begin(localPort);

}

void loop() {
  
  int packetSize = Udp.parsePacket();  

  if (packetSize) {

    // ignore artnet dmx header
    //Udp.read((char*)0, 18);

    Udp.read((char*)leds[0], LEDS_PER_STRING * 3);
    Udp.read((char*)leds[1], LEDS_PER_STRING * 3);
    Udp.read((char*)leds[2], LEDS_PER_STRING * 3);
    Udp.read((char*)leds[3], LEDS_PER_STRING * 3);

  }
  FastLED.show();

}
