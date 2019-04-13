from numpy.random import uniform, randint
from numpy import array, zeros, empty, uint8, append, argsort
from math import cos, sin, radians, floor
from numba import njit, prange
import cfg

# canvas_palette = [
#     [95,  # wall
#      99,
#      84]
# ]
# 
# palette = [
#     [207,  # wall
#      207,
#      207],
#     [178,  # skin
#      121,
#      91],
#     [75,  # shirt
#      84,
#      76],
#     [79,    # eye
#      71,
#      60],
#     [48,
#      56,
#      48],
#     [110,   # lips
#      70,
#      62],
#     [211,   # transm, cheek
#      169,
#      153]
# ]

# canvas_palette = [
#     [27,
#      23,
#      22]
# ]
#
# palette = [
#     [53,
#      53,
#      53]
# ]

# canvas_palette = [
#     [204,
#      204,
#      204]
# ]
#
# palette = [
#     [92,
#      92,
#      92]
# ]

canvas_palette = [
    [234,
     238,
     239],
    [116,
     146,
     218]
]

palette = [
    # [108,
    #  68,
    #  137],
    # [84,
    #  123,
    #  190],
    # [209,
    #  211,
    #  210],
    [144,
     42,
     89],
    [50,
     29,
     98]
    # [185,
    #  57,
    #  82],
    # [220,
    #  220,
    #  220]
]

# canvas_palette = [
#     [0,
#      156,
#      200]
# ]
#
# palette = [
#     [0,
#      0,
#      0],
#     [0,
#      0,
#      112],
#     [4,
#      13,
#      142],
#     [123,
#      204,
#      255],
#     [220,
#      250,
#      255]
# ]

canvas_palette = array([array(x) for x in canvas_palette])
palette = array([array(x) for x in palette])


def gen_population(pop_size, size):
    population = zeros((pop_size, size[0], size[1], cfg.n_color_ch), dtype=uint8)
    for i in range(pop_size):
        population[i] = get_canvas(size[0], size[1])
    return population


def get_best():
    indices = argsort(cfg.fitness)
    return cfg.new_population[indices[0]], indices[0]


@njit(parallel=False)
def crossover(parents, n_parents, size, offspring_size):
    offspring = zeros((offspring_size, size[0], size[1], cfg.n_color_ch), dtype=uint8)
    crossover_point = uint8(size[0] / 2)
    for k in range(offspring_size):
        parent1_idx = int((n_parents - 1) * uniform(0, 1) ** 2)
        parent2_idx = int((n_parents - 1) * uniform(0, 1) ** 2)
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring


@njit(parallel=False)
def mutation(offspring_crossover, size, offspring_size, length):
    # offspring = zeros((offspring_size, size[0], size[1], 4))
    for i in range(offspring_size):
        if uniform(0, 1) > 0.9: continue
        offspring_crossover[i] = draw_stroke(offspring_crossover[i], length, size[0], size[1])
    return offspring_crossover


@njit(parallel=True)
def cal_pop_fitness(population, target):
    fitness = zeros(shape=cfg.pop_size)
    for x in range(len(population)):
        distance = 0
        for i in prange(population[x].shape[0]):
            for j in range(population[x].shape[1]):
                for k in range(3):
                    distance += (int(population[x][i, j, k]) - int(target[i, j, k])) ** 2
        fitness[x] = distance
    return fitness


@njit(parallel=True)
def select_mating_pool(population, fitness, n_parents):
    x_bound = population[0].shape[0]
    y_bound = population[0].shape[1]
    rgb = population[0].shape[2]
    parents = zeros((n_parents, x_bound, y_bound, rgb))
    indices = argsort(fitness)
    for i in prange(n_parents):
        parents[i] = population[indices[i]]
    return parents


@njit(parallel=False)
def get_canvas(x_bound, y_bound):
    canvas = zeros(shape=(x_bound, y_bound, cfg.n_color_ch), dtype=uint8)

    a = randint(len(canvas_palette))
    colors = canvas_palette[a]
    for i in range(x_bound):
        for j in range(y_bound):
            canvas[i, j, 0], \
            canvas[i, j, 1], \
            canvas[i, j, 2] = colors
    return canvas


@njit(parallel=False)
def draw_stroke(canvas, length, x_bound, y_bound):
    x0 = randint(0, x_bound - 5)
    y0 = randint(0, y_bound - 5)
    angle = radians(uniform(0, 360))
    x1 = (int(length * cos(angle) + x0))
    y1 = (int(length * sin(angle) + y0))
    # don't care about the angle yet

    a = randint(len(palette))
    fill = palette[a]

    alpha = 0.12
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    # print('Actual length is {}'.format(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** (1/2)))
    pixels = interpolate_pixels_along_line(x0, y0, min(x1, x_bound - 2), min(y1, y_bound - 2))

    for i, j in pixels:
        canvas[i, j] = fill * alpha + canvas[i, j] * (1 - alpha)
    return canvas


"""
    The code below comes from https://stackoverflow.com/questions/24702868/python3-pillow-get-all-pixels-on-a-line
"""


@njit(parallel=False)
def interpolate_pixels_along_line(x0, y0, x1, y1):
    """Uses Xiaolin Wu's line algorithm to interpolate all of the pixels along a
    straight line, given two points (x0, y0) and (x1, y1)

    Wikipedia article containing pseudo code that function was based off of:
        http://en.wikipedia.org/wiki/Xiaolin_Wu's_line_algorithm
    """
    pixels = []
    steep = abs(y1 - y0) > abs(x1 - x0)

    # Ensure that the path to be interpolated is shallow and from left to right
    if steep:
        t = x0
        x0 = y0
        y0 = t

        t = x1
        x1 = y1
        y1 = t

    if x0 > x1:
        t = x0
        x0 = x1
        x1 = t

        t = y0
        y0 = y1
        y1 = t

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx  # slope

    # Get the first given coordinate and add it to the return list
    x_end = round(x0)
    y_end = y0 + (gradient * (x_end - x0))
    xpxl0 = x_end
    ypxl0 = round(y_end)
    if steep:
        pixels.extend([(ypxl0, xpxl0), (ypxl0 + 1, xpxl0)])
    else:
        pixels.extend([(xpxl0, ypxl0), (xpxl0, ypxl0 + 1)])

    interpolated_y = y_end + gradient

    # Get the second given coordinate to give the main loop a range
    x_end = round(x1)
    y_end = y1 + (gradient * (x_end - x1))
    xpxl1 = x_end
    ypxl1 = round(y_end)

    # Loop between the first x coordinate and the second x coordinate, interpolating the y coordinates
    for x in range(xpxl0 + 1, xpxl1):
        if steep:
            pixels.extend([(floor(interpolated_y), x), (floor(interpolated_y) + 1, x)])

        else:
            pixels.extend([(x, floor(interpolated_y)), (x, floor(interpolated_y) + 1)])

        interpolated_y += gradient

    # Add the second given coordinate to the given list
    if steep:
        pixels.extend([(ypxl1, xpxl1), (ypxl1 + 1, xpxl1)])
    else:
        pixels.extend([(xpxl1, ypxl1), (xpxl1, ypxl1 + 1)])

    return pixels
