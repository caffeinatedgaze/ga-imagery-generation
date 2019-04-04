from PIL import Image

orig = Image.open('src/circle_black.jpg')

x_bound, y_bound = orig.size

population = []
prime = None  # the best program is here

n_quads = 1024
length = 1
pop_size = 4
