from numpy.random import randint, normal, uniform
from PIL import Image, ImageDraw
# from random import randint
from math import sin, cos
import cfg


#
# quads (x, y, width, greyscale)
#

class Chromosome:

    def __init__(self, n):
        self.strokes = []
        self.fitness = -1
        self.n = n
        random_var = randint(0, 10)
        if random_var <= 1:
            print('Uniform')
            self.gen_uniform()
        elif 1 < random_var <= 7:
            print('Normal')
            self.gen_normal()
        elif 7 < random_var <= 8:
            print('Lower')
            self.gen_lower()
        else:
            print('Upper')
            self.gen_upper()

    def gen_normal(self):
        for i in range(self.n):
            self.strokes.append(self.get_stroke_normal(cfg.length, cfg.x_bound, cfg.x_bound))

    def gen_uniform(self):
        for i in range(self.n):
            self.strokes.append(self.get_stroke_uniform(cfg.length, (0, cfg.x_bound), (0, cfg.y_bound)))

    def gen_lower(self):
        for i in range(self.n):
            self.strokes.append(self.get_stroke_uniform(cfg.length, (0, cfg.x_bound),
                                                        (0, cfg.y_bound // 2)))

    def gen_upper(self):
        for i in range(self.n):
            self.strokes.append(self.get_stroke_uniform(cfg.length, (0, cfg.x_bound),
                                                        (cfg.y_bound // 2, cfg.y_bound)))

    @staticmethod
    def get_stroke_normal(length, x_bound, y_bound):
        x0 = normal(x_bound // 2, x_bound // 8)
        y0 = normal(y_bound // 2, y_bound // 8)
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
    def get_stroke_uniform(length, x_boundaries, y_boundaries):
        x0 = uniform(x_boundaries[0], x_boundaries[1])
        y0 = uniform(y_boundaries[0], y_boundaries[1])
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
