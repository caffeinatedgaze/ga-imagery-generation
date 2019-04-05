from numpy import array, zeros
from PIL import Image

orig = Image.open('src/circle_black.jpg')
target = array(orig)

x_bound, y_bound = orig.size

n_strokes = 256
length = 64
pop_size = 128
mating_size = 16
crossover_size = pop_size - mating_size

new_population = []
parents = []
offspring_crossover = []
offspring_mutation = []
fitness = []
