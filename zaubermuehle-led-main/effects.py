import random

import time

from leds import fade_color

COLORS = [
    (244, 67, 54),   # Red
    (232, 30, 99),   # Pink
    (156, 39, 176),  # Purple
    (103, 58, 183),  # Deep Purple
    (63, 81, 181),   # Indigo
    (33, 150, 243),  # Blue
    (3, 169, 244),   # Light Blue
    (0, 188, 212),   # Cyan
    (0, 150, 136),   # Teal
    (76, 175, 80),   # Green
    (139, 195, 74),  # Light Green
    (205, 220, 57),  # Lime
    (255, 235, 59),  # Yellow
    (255, 193, 7),   # Amber
    (255, 152, 0),   # Orange
    (255, 87, 34)    # Deep Orange
]

COLORS2 = [
    (255,0,0),
    (0,255,0),
    (0,0,255)
]


class Effect:

    def __init__(self, leds, speed=1.0):
        self.leds = leds
        self.speed = speed

    def tick(self):
        time.sleep(0.0001)


class KickTriggeredEffect(Effect):

    def kick(self):
        pass

class KickTriggeredUnicolor(KickTriggeredEffect):

    def kick(self):

        for cube in self.leds.cubes:
            cube.set_color(random.choice(COLORS))

        self.leds.show()


class ChaseEffect(Effect):

    def tick(self):
        color = random.choice(COLORS)

        for cube in self.leds.cubes:

            self.leds.clear()
            cube.set_color(color)
            self.leds.show()

            time.sleep(0.3/self.speed)


class UnicolorEffect(Effect):

    def tick(self):

        for cube in self.leds.cubes:
            cube.set_color(random.choice(COLORS))

        self.leds.show()

        time.sleep(0.3/self.speed)


class StrobeEffect(Effect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggle = True

    def tick(self):

        for cube in self.leds.cubes:
            cube.set_color(random.choice(COLORS) if self.toggle else (0, 0, 0))

        self.leds.show()

        time.sleep((1.0/20) / self.speed)

        self.toggle = not self.toggle


class RotationEffect(Effect):

    def tick(self):

        color = random.choice(COLORS)

        for pos in range(120):

            pos /= 10

            self.leds.clear()

            for x in range(12):
                distance = abs(pos-x)

                if distance <= 1.0:
                    output_color = color
                elif distance < 4:
                    output_color = fade_color(color, 0.3/distance)
                    #output_color = (0, 0, 0)
                else:
                    output_color = (0, 0, 0)

                for cube in self.leds.cubes:
                    if x < 3:
                        side = cube.left
                    elif x < 6:
                        side = cube.front
                    elif x < 9:
                        side = cube.right
                    else:
                        side = cube.back
                    side[x % 3][0] = output_color
                    side[x % 3][1] = output_color
                    side[x % 3][2] = output_color

            self.leds.show()
            time.sleep(0.003 / self.speed)


class PulseEffect(Effect):


    def tick(self):

        for i in range(5):

            for cube in self.leds.cubes:

                color = random.choice(COLORS)

                if i == 0:
                    side = cube.left
                elif i == 1:
                    side = cube.right
                elif i == 2:
                    side = cube.bottom
                elif i == 3:
                    side = cube.back
                elif i == 4:
                    side = cube.front

                for x in range(3):
                    for y in range(3):
                        side[x][y] = color

            self.leds.show()
            time.sleep(1.0/10*self.speed)

class RainbowEffect(Effect):

    def tick(self):
        for i in range(len(COLORS)):
            for cube_index, cube in enumerate(self.leds.cubes):
                cube.set_color(COLORS[(i + cube_index) % len(COLORS)])
            self.leds.show()
            time.sleep(0.3/self.speed)

class FadeEffect(Effect):

    def tick(self):
        for cube in self.leds.cubes:
            target_color = random.choice(COLORS)
            fade_color(cube, target_color, duration=1.0/self.speed)
        self.leds.show()
        time.sleep(1.1/self.speed)  # Wait for fade to complete

class BlinkEffect(Effect):

    def tick(self):
        for cube in self.leds.cubes:
            cube.set_color(random.choice(COLORS))
        self.leds.show()
        time.sleep(0.5/self.speed)
        self.leds.clear()
        self.leds.show()
        time.sleep(0.5/self.speed)

class ColorExplosionEffect(KickTriggeredEffect):

    def kick(self):
        for cube in self.leds.cubes:
            for _ in range(10):
                cube.set_color(random.choice(COLORS))
                self.leds.show()
                time.sleep(0.1/self.speed)
            cube.set_color((0, 0, 0))  # Turn off the cube after explosion
        self.leds.show()

class RandomChaseEffect(KickTriggeredEffect):

    def kick(self):
        start_cube = random.choice(self.leds.cubes)
        color = random.choice(COLORS)
        for _ in range(10):
            for cube in self.leds.cubes:
                cube.set_color((0, 0, 0))  # Clear all cubes
            start_cube.set_color(color)
            self.leds.show()
            time.sleep(0.3/self.speed)
            start_cube = random.choice(self.leds.cubes)
            color = random.choice(COLORS)

class ColorWaveEffect(KickTriggeredEffect):

    def kick(self):
        wave_colors = [random.choice(COLORS) for _ in range(len(self.leds.cubes))]
        for color in wave_colors:
            for cube in self.leds.cubes:
                cube.set_color(color)
            self.leds.show()
            time.sleep(0.2/self.speed)
        for cube in self.leds.cubes:
            cube.set_color((0, 0, 0))  # Turn off all cubes after the wave passes
        self.leds.show()

class ColorStrobeEffect(KickTriggeredEffect):

    def kick(self):
        color1 = random.choice(COLORS)
        color2 = random.choice(COLORS)
        for _ in range(10):
            for cube in self.leds.cubes:
                cube.set_color(color1)
            self.leds.show()
            time.sleep(0.1/self.speed)
            for cube in self.leds.cubes:
                cube.set_color(color2)
            self.leds.show()
            time.sleep(0.1/self.speed)

class ColorPulseEffect(KickTriggeredEffect):

    def kick(self):
        color = random.choice(COLORS)
        for _ in range(5):
            for i in range(50, 255, 10):
                for cube in self.leds.cubes:
                    cube.set_color((color[0]*i//255, color[1]*i//255, color[2]*i//255))
                self.leds.show()
                time.sleep(0.05/self.speed)
            for i in range(255, 50, -10):
                for cube in self.leds.cubes:
                    cube.set_color((color[0]*i//255, color[1]*i//255, color[2]*i//255))
                self.leds.show()
                time.sleep(0.05/self.speed)

class ColorRainEffect(KickTriggeredEffect):

    def kick(self):
        for _ in range(20):
            for cube in self.leds.cubes:
                cube.set_color((0, 0, 0))  # Clear all cubes
            for _ in range(random.randint(1, 5)):
                cube = random.choice(self.leds.cubes)
                cube.set_color(random.choice(COLORS))
            self.leds.show()
            time.sleep(0.1/self.speed)

class RotationEffect2(Effect):

    def tick(self):
        color = random.choice(COLORS)
        
        for pos in range(120):
            pos /= 10

            self.leds.clear()

            for x in range(12):
                distance = abs(pos - x)

                if distance <= 1.0:
                    output_color = color
                elif distance < 4:
                    # Smooth fade for colors further away
                    output_color = fade_color(color, 0.3 / distance)
                else:
                    output_color = (0, 0, 0)

                for cube in self.leds.cubes:
                    if x < 3:
                        side = cube.left
                    elif x < 6:
                        side = cube.front
                    elif x < 9:
                        side = cube.right
                    else:
                        side = cube.back

                    for y in range(3):
                        side[y] = [output_color for _ in range(3)]

            self.leds.show()
            time.sleep(0.003 / self.speed)


