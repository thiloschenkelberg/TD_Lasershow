
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

#define CUBES           8
#define SIDES_PER_CUBE  5
#define SIDE_WIDTH      3
#define SIDE_HEIGHT     SIDE_WIDTH

#define SIDE_FRONT      0
#define SIDE_LEFT       1
#define SIDE_BACK       2
#define SIDE_RIGHT      3
#define SIDE_BOTTOM     4

//#define LED_STRINGS     4
#define CUBES_PER_STRING 90
#define LEDS_PER_STRING 2*SIDES_PER_CUBE*SIDE_WIDTH*SIDE_WIDTH

#define DATA_PIN_1    6
#define DATA_PIN_2    8
#define DATA_PIN_3    10
#define DATA_PIN_4    12


CRGB COLORS[] = {
  CRGB::Red,
  CRGB::Green,
  CRGB::Blue
};


// 2 cubes per string
CRGB leds[CUBES/2][LEDS_PER_STRING];

#define OVERALL_BRIGHTNESS  255


byte led_map[CUBES][SIDES_PER_CUBE][SIDE_WIDTH][SIDE_HEIGHT];

void calc_map() {
  for (int cube=0;cube<2;cube++) {
    for (int side=0;side<SIDES_PER_CUBE;side++) {
      for (int x=0;x<SIDE_WIDTH;x++) {
        for (int y=0;y<SIDE_HEIGHT;y++) {

          int addr = cube * SIDES_PER_CUBE * SIDE_WIDTH * SIDE_HEIGHT;
          addr += side * SIDE_WIDTH * SIDE_HEIGHT;
          addr += y * 3;

          if (y == 1) {
            addr += (2-x);
          } else {
            addr += x;
          }

          led_map[cube][side][x][y] = addr;

        }
      }
    }
  }
}

void leds_clear() {
  memset(leds, 0x00, sizeof(leds));
}

void set(int cube, int side, int x, int y, CRGB color) {
  leds[cube / 2][led_map[cube%2][side][x][y]] = color;
}

void effect_rotate() {

  CRGB color = COLORS[int(random(0, 3))];
  static int sides[] = {1, 0, 3, 2};

  for (int pos=0;pos<12;pos++) {

      for (int x=0;x<12;x++) {

        int distance = abs(pos-x);

        CRGB output_color;
        if (distance <= 1) {
            output_color = color;
        //else if (distance < 4)
            //output_color = fade_color(color, 0.3/distance)
            //#output_color = (0, 0, 0)
        } else {
            output_color = CRGB::Black;
        }

        byte x_ = x%3;

        for (int cube=0;cube<CUBES;cube++) {
            set(cube, sides[x/3], x_, 0, output_color);
            set(cube, sides[x/3], x_, 1, output_color);
            set(cube, sides[x/3], x_, 2, output_color);
        }
      }

      FastLED.show();
      delay(30);
  }
}


char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
EthernetUDP Udp;


void setup() {

  calc_map();

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

effect_rotate();
 return;


  int packetSize = Udp.parsePacket();

  if (packetSize) {

    // ignore artnet dmx header
    Udp.read((char*)0, 18);

    Udp.read((char*)leds[0], LEDS_PER_STRING * 3);
    Udp.read((char*)leds[1], LEDS_PER_STRING * 3);
    Udp.read((char*)leds[2], LEDS_PER_STRING * 3);
    Udp.read((char*)leds[3], LEDS_PER_STRING * 3);

  }
  FastLED.show();

}
