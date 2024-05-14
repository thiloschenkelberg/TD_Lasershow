
import random
import socket
import time
from queue import Queue, Empty
from threading import Thread

from effects import *

from leds import Installation

ARDUINO_UDP_IP = "192.168.11.100"
ARDUINO_UDP_PORT = 3456


LOCAL_UDP_IP = "127.0.0.1" # 127.0.0.1 for local
LOCAL_UDP_PORT = 6543

leds = Installation(8, ARDUINO_UDP_IP, ARDUINO_UDP_PORT)


leds.brightness = 0.1

EFFECTS = [
    #KickTriggeredUnicolor,
    #ChaseEffect,
    #UnicolorEffect,
    #StrobeEffect,
    PulseEffect,
    #RotationEffect,
    #RainbowEffect,
    #FadeEffect,            
    #BlinkEffect,
    #ColorExplosionEffect,
    #RandomChaseEffect,
    #ColorWaveEffect,
    #ColorStrobeEffect,
    #ColorPulseEffect,
    #ColorRainEffect,
    #RotationEffect2,
    #ColorWaveEffect2,
    #ColorWaveEffect3,
    #ColorRandomBlinkEffect,
    #KickTriggeredPlanets,
    #PulsatingPlanets,
    #RotatingPlanets

]

EFFECT_TIME = 4.0 # s

def network_thread(kick_queue):

    recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    recv_sock.bind((LOCAL_UDP_IP, LOCAL_UDP_PORT))

    last_val = 0

    while True:
        # 18 bytes artnet header
        data, addr = recv_sock.recvfrom(19)
        if last_val != data[-1]:
            last_val = data[-1]
            kick_queue.put(data)

def effect_thread(kick_queue):

    while True:

        effect = random.choice(EFFECTS)(leds, speed=1.0)
        start = time.time()

        while time.time() - start < EFFECT_TIME:
            effect.tick()
            try:
                kick_queue.get(block=False)
                if isinstance(effect, KickTriggeredEffect):
                    effect.kick()
            except Empty:
                pass


kick_queue = Queue()

t1 = Thread(target=effect_thread, args =(kick_queue, ))
t2 = Thread(target=network_thread, args =(kick_queue, ))

t1.start()
t2.start()

t1.join()
t2.join()
