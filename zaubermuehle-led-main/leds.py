import socket

def init_side(color=(0, 0, 0)):

    return [
        [color, color, color],
        [color, color, color],
        [color, color, color]
    ]


def output_map_side(data):
    # 1 2 3
    # 6 5 4 -> 1,2,3,4,5,5,6,7,8,9
    # 7 8 9
    data = [
        data[0][0], data[1][0], data[2][0],
        data[2][1], data[1][1], data[0][1],
        data[0][2], data[1][2], data[2][2],
    ]

    output = []

    for d in data:
        output += d

    return output

def fade_color(color, fade):
    return int(color[0]*fade), int(color[1] * fade), int(color[2] * fade)

class Cube:

    def __init__(self):
        self.clear()

    def clear(self):
        self.set_color((0, 0, 0))

    def set_color(self, color):
        self.left = init_side(color)
        self.right = init_side(color)
        self.front = init_side(color)
        self.back = init_side(color)
        self.bottom = init_side(color)

    @property
    def data(self):
        return (
            output_map_side(self.front) +
            output_map_side(self.left) +
            output_map_side(self.back) +
            output_map_side(self.right) +
            output_map_side(self.bottom)
        )

class Installation:

    def __init__(self, cubes, udp_ip, udp_port):
        self.cubes = [Cube() for i in range(cubes)]
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.brightness = 1.0

    def show(self):

        data = []
        for cube in self.cubes:
            data += cube.data

        if self.brightness != 1.0:
            data = [int(d * self.brightness) for d in data]

        # front, left, back, right
        self.socket.sendto(bytearray(data), (self.udp_ip, self.udp_port))

    def clear(self):
        for cube in self.cubes:
            cube.clear()

    def set_color(self, color):
        for cube in self.cubes:
            cube.set_color(color)