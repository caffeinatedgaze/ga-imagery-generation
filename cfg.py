from PIL import Image

orig = Image.open('src/tree_tiny.jpg')

x_bound, y_bound = orig.size

population = []
prime = None  # the best program is here

n_quads = 4096
length = 1
pop_size = 4  # don't change it
