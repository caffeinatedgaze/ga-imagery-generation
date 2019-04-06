from numpy import array, zeros
from PIL import Image

orig = Image.open('src/default_tiny.jpg')
target = array(orig)

y_bound, x_bound = orig.size

n_strokes = 16
length = 1
pop_size = 64
mating_size = 32
crossover_size = pop_size - mating_size

new_population = []
parents = []
offspring_crossover = []
offspring_mutation = []
fitness = []
