from numpy.random import randint, normal, uniform
from PIL import Image, ImageDraw
# from random import randint
from math import sin, cos
import cfg


#
# quads (x, y, width, greyscale)
#

class Chromosome:

    def __init__(self, n, func):
        self.strokes = []
        self.fitness = -1
        for i in range(n):
            self.strokes.append(func(cfg.length))

    @staticmethod
    def get_stroke_normal(length):
        x0 = normal(cfg.x_bound // 2, cfg.x_bound // 6)
        y0 = normal(cfg.y_bound // 2, cfg.y_bound // 6)
        angle = randint(1, 360) / 100
        # angle = 1
        x1 = length * cos(angle) + x0
        y1 = length * sin(angle) + y0
        width = 1
        fill = (0,
                0,
                0,
                randint(254, 255))
        return [x0, y0, x1, y1], fill, width

    @staticmethod
    def get_stroke_uniform(length):
        x0 = uniform(0, cfg.x_bound)
        y0 = uniform(0, cfg.y_bound)
        angle = randint(1, 360) / 100
        # angle = 1
        x1 = length * cos(angle) + x0
        y1 = length * sin(angle) + y0
        width = 1
        fill = (0,
                0,
                0,
                randint(254, 255))
        return [x0, y0, x1, y1], fill, width

    def generate(self):
        image = Image.new('RGBA', size=(cfg.x_bound, cfg.y_bound), color=(255, 255, 255, 255))
        draw = ImageDraw.Draw(image)
        for stroke in self.strokes:
            x0 = stroke[0][0]
            y0 = stroke[0][1]
            x1 = stroke[0][2]
            y1 = stroke[0][3]
            draw.line((x0, y0, x1, y1), stroke[1], stroke[2])
        return image
