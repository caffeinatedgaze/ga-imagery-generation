from PIL import Image, ImageDraw
from random import randint


#
# quads (x, y, width, greyscale)
#

class Chromosome:
    x_bound: int
    y_bound: int

    def __init__(self, n, im_size):
        global x_bound, y_bound
        x_bound = im_size[0]
        y_bound = im_size[1]
        self.strokes = []
        for i in range(n):
            self.strokes.append(self.get_stroke())

    @staticmethod
    def get_stroke():
        x0 = randint(0, x_bound)
        x1 = randint(0, x_bound)
        y0 = randint(0, y_bound)
        y1 = randint(0, y_bound)
        width = 1
        fill = (0,
                0,
                0,
                randint(128, 255))

        return [x0, y0, x1, y1], fill, width

    def generate(self):
        image = Image.new('RGBA', size=(x_bound, y_bound), color=(64, 128, 128, 255))
        draw = ImageDraw.Draw(image)
        for stroke in self.strokes:
            x0 = stroke[0][0]
            y0 = stroke[0][1]
            x1 = stroke[0][2]
            y1 = stroke[0][3]
            draw.line((x0, y0, x1, y1), stroke[1], stroke[2])
        return image
