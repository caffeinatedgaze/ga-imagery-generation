from PIL import Image, ImageDraw
from time import time, clock
import random

#
# quads (x, y, width, greyscale)
#

im_size = (300, 300)


class Chromosome:

    def __init__(self, n, x_bound=im_size[0], y_bound=im_size[1]):
        self.strokes = []
        # random.seed(clock())
        for i in range(n):
            x0 = random.randint(0, x_bound)
            x1 = random.randint(0, x_bound)
            y0 = random.randint(0, y_bound)
            y1 = random.randint(0, y_bound)
            width = 2
            fill = (0,
                    0,
                    0,
                    random.randint(128, 255))
            self.strokes.append(
                ([x0, y0, x1, y1], fill, width))

    def generate(self):
        image = Image.new('RGBA', size=im_size, color=(64, 128, 128, 255))
        draw = ImageDraw.Draw(image)
        for stroke in self.strokes:
            x0 = stroke[0][0]
            y0 = stroke[0][1]
            x1 = stroke[0][2]
            y1 = stroke[0][3]
            draw.line((x0, y0, x1, y1), stroke[1], stroke[2])
        return image


class GA:
    orig: Image
    n_strokes: int
    pop_size: int
    pop: list
    fitness: list

    @staticmethod
    def set_params(canonical_im, p_size=3, n_strks=1024):
        global orig, pop_size, n_strokes, fitness
        orig = canonical_im
        pop_size = p_size
        n_strokes = n_strks

    @staticmethod
    def gen_init_pop():
        global pop, pop_size, n_strokes
        pop = [Chromosome(n_strokes) for _ in range(pop_size)]

    @staticmethod
    def cal_pop_fitness():
        global fitness
        fitness = [GA.euclide(x.generate()) for x in pop]

    @staticmethod
    def euclide(im):
        global orig
        if orig.size != im.size:
            raise Exception('Images should be of equal size\n{} and the one being generated are not'.
                            format(orig.filename))
        width, height = orig.size
        distance = 0

        for x in range(width):
            for y in range(height):
                r1, g1, b1 = orig.getpixel((x, y))
                r2, g2, b2, _ = im.getpixel((x, y))
                distance += ((r1 + g1 + b1) - (r2 + g2 + b2)) ** 2
        return distance

    @staticmethod
    def get_fit():
        return fitness

    @staticmethod
    def get_pop():
        return pop

    @staticmethod
    def pop_show():
        global pop
        for ch in pop:
            ch.generate().save('src/strokes.png', 'PNG')


def main():
    start = time()
    GA.set_params(Image.open('src/default.jpg'),
                  p_size=10,
                  n_strks=8192)
    GA.gen_init_pop()
    GA.cal_pop_fitness()
    GA.pop_show()
    print(GA.get_fit())
    print('%.6f seconds' % (time() - start))


if __name__ == '__main__':
    main()
