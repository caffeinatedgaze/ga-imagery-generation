from PIL import Image

orig = Image.open('src/circle_black_tiny.jpg')

x_bound, y_bound = orig.size

population = []
prime = None  # the best program is here

n_quads = 64
length = 1
pop_size = 64
