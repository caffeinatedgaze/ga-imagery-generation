from PIL import Image, ImageFilter

im = Image.open('/strg/ga-imagery-generation/default.png')
im.show()

im_sharp = im.filter(ImageFilter.SHARPEN)
# im_sharp.show()

r, g, b = im_sharp.split()
