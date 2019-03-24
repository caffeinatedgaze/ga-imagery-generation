from PIL import Image
import os

original = Image.open('/strg/ga-imagery-generation/src/default.jpg')


def compute_distance(im1, im2):
    if im1.size != im2.size:
        raise Exception('Images should be of equal size\n{} and {} are not'.
                        format(im1.filename, im2.filename))

    width, height = im1.size
    distance = 0

    for x in range(width):
        for y in range(height):
            r1, g1, b1 = im1.getpixel((x, y))
            r2, g2, b2 = im2.getpixel((x, y))
            distance += ((r1 + g1 + b1) - (r2 + g2 + b2)) ** 2
    return distance


directory = '/strg/ga-imagery-generation/src/'
results = []

for pic in os.listdir(directory):
    if pic.endswith('.jpg'):
        image = Image.open(directory + pic)
        results.append((pic, compute_distance(image, original)))

for item in sorted(results, key=lambda x: x[1]):
    print('{0:32}{1}'.format(item[0], item[1]))

# default.jpg                     0
# green_hue_max.jpg               1054896
# small_dot.jpg                   5625244
# posterize_13.jpg                11565293
# lil_curve.jpg                   366959592
# max_contrast.jpg                2034139623
# contrast_min.jpg                3138894074
