from numpy import array, zeros
from PIL import Image

orig = Image.open('contest/target.jpeg')
target = array(orig)

y_bound, x_bound = orig.size

n_strokes = 255
length = 64 

pop_size = 32 
mating_size = 18 
crossover_size = pop_size - mating_size

n_color_ch = 3

new_population = []
parents = []
offspring_crossover = []
offspring_mutation = []
fitness = []


# 34 min of 10 pm
