from numpy.random import randint, normal, uniform, choice
from math import sin, cos, radians
from PIL import Image, ImageDraw
import cfg


#
# quads (x, y, width, greyscale)
#

class Chromosome:

    def __init__(self, n):
        self.program = []
        self.fitness = -1
        self.n = n
        self.type = ''
        gen_func = [self.gen_uniform, self.gen_normal,
                    self.gen_lower, self.gen_upper]
        distribution = [1, 0, 0, 0]
        index = choice(cfg.pop_size, None, replace=False, p=distribution)
        gen_func[index]()

        # todo: do the python-way

    @staticmethod
    def get_quad_normal(length, x_bound, y_bound):
        x0 = normal(x_bound // 2, x_bound // 8)
        y0 = normal(y_bound // 2, y_bound // 8)
        angle = radians(randint(0, 360))
        x1 = length * cos(angle) + x0
        y1 = length * sin(angle) + y0
        width = 1
        fill = (0,
                0,
                0,
                randint(32, 255))
        return [x0, y0, x1, y1], fill, width

    @staticmethod
    def get_quad_uniform(length, x_boundaries, y_boundaries):
        x0 = uniform(x_boundaries[0], x_boundaries[1])
        y0 = uniform(y_boundaries[0], y_boundaries[1])
        angle = radians(randint(0, 360))
        x1 = length * cos(angle) + x0
        y1 = length * sin(angle) + y0
        width = 1
        fill = (0,
                0,
                0,
                randint(32, 255))
        return [x0, y0, x1, y1], fill, width

    def execute(self):
        image = Image.new('RGBA', size=(cfg.x_bound, cfg.y_bound), color=(255, 255, 255, 255))
        draw = ImageDraw.Draw(image)
        for quad in self.program:
            x0 = quad[0][0]
            y0 = quad[0][1]
            x1 = quad[0][2]
            y1 = quad[0][3]
            draw.line((x0, y0, x1, y1), quad[1], quad[2])
        return image

    def gen_normal(self):
        self.type = 'normal'
        for i in range(self.n):
            self.program.append(self.get_quad_normal(cfg.length, cfg.x_bound, cfg.x_bound))

    def gen_uniform(self):
        self.type = 'uniform'
        for i in range(self.n):
            self.program.append(self.get_quad_uniform(cfg.length, (0, cfg.x_bound), (0, cfg.y_bound)))

    def gen_lower(self):
        self.type = 'lower'
        for i in range(self.n):
            self.program.append(self.get_quad_uniform(cfg.length, (0, cfg.x_bound),
                                                      (0, cfg.y_bound // 2)))

    def gen_upper(self):
        self.type = 'upper'
        for i in range(self.n):
            self.program.append(self.get_quad_uniform(cfg.length, (0, cfg.x_bound),
                                                      (cfg.y_bound // 2, cfg.y_bound)))
