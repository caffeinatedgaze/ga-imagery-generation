from PIL import Image

im_before = Image.open('/strg/ga-imagery-generation/src/default.jpg')
im_after  = Image.open('/strg/ga-imagery-generation/src/posterize_13.jpg')


def compute_distance(im1, im2):

    width, height = im_before.size
    distance = 0

    for x in range(width):
        for y in range(height):
            r1, g1, b1 = im1.getpixel((x, y))
            r2, g2, b2 = im2.getpixel((x, y))
            distance += ((r1 + g1 + b1) - (r2 + g2 + b2))**2
    return distance


print(compute_distance(im_before, im_after))

# 5228711
# 1054896           -> max green hue
# 8959576           -> max saturation
# 11565293          -> posterize 13
# 285206550
# 573377762
# 1925280624
# 4772632775        -> max brightness
