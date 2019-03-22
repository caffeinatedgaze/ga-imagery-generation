from PIL import Image, ImageFilter

im = Image.open('/strg/ga-imagery-generation/default.png')
# im.show()

im_sharp = im.filter(ImageFilter.SHARPEN)
# im_sharp.show()

width, height = im.size
for x in range(width):
    for y in range(height):
        r, g, b = im.getpixel((x, y))
        print(r, g, b)
