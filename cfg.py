from PIL import Image

orig = Image.open('src/tree_lossy.jpg')
im_size = orig.size
n_strokes = 512
length = 24
pop_size = 3
population = []
next_pop = []
fitness = []
