from numpy import array, zeros
from PIL import Image

orig = Image.open('src/default.jpg')
target = array(orig)

y_bound, x_bound = orig.size

n_strokes = 255
length = 24
pop_size = 4
mating_size = 1
crossover_size = pop_size - mating_size

n_color_ch = 4

new_population = []
parents = []
offspring_crossover = []
offspring_mutation = []
fitness = []
