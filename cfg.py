from PIL import Image

orig = Image.open('src/circle_black.jpg')
im_size = orig.size
x_bound = im_size[0]
y_bound = im_size[1]
n_strokes = 1024
length = 1
pop_size = 16
population = []
next_pop = []
fitness = []
