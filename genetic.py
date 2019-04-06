from numpy.random import uniform, randint
from numpy import array, zeros, empty, uint8, append, argsort
from math import cos, sin, radians
from numba import njit, prange
import cfg


def gen_population(pop_size, size):
    population = zeros((pop_size, size[0], size[1], 3), dtype=uint8)
    for i in range(pop_size):
        population[i] = get_canvas(size[0], size[1])
    return population


def get_best():
    indices = argsort(cfg.fitness)
    return cfg.new_population[indices[0]]


@njit(parallel=False)
def crossover(parents, n_parents, size, offspring_size):
    offspring = zeros((offspring_size, size[0], size[1], 3), dtype=uint8)
    crossover_point = uint8(size[0] / 2)
    for k in range(offspring_size):
        parent1_idx = int((n_parents - 1) * uniform(0, 1) ** 2)
        parent2_idx = int((n_parents - 1) * uniform(0, 1) ** 2)
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring


@njit
def mutation(offspring_crossover, size, offspring_size, length):
    # offspring = zeros((offspring_size, size[0], size[1], 4))
    for i in range(offspring_size):
        if uniform(0, 1) > 0.9: continue
        offspring_crossover[i] = draw_stroke(offspring_crossover[i], length, size[0], size[1])
    return offspring_crossover


@njit(parallel=False)
def cal_pop_fitness(population, target):
    fitness = zeros(shape=cfg.pop_size)
    for x in range(len(population)):
        distance = 0
        for i in range(population[x].shape[0]):
            for j in range(population[x].shape[1]):
                for k in range(3):
                    distance += abs(int(population[x][i, j, k]) - int(target[i, j, k]) // 3)
        fitness[x] = distance
    return fitness


@njit(parallel=False)
def select_mating_pool(population, fitness, n_parents):
    x_bound = population[0].shape[0]
    y_bound = population[0].shape[1]
    rgb = population[0].shape[2]
    parents = zeros((n_parents, x_bound, y_bound, rgb))
    indices = argsort(fitness)
    for i in range(n_parents):
        parents[i] = population[indices[i]]
    return parents


#
# Code that generates a programargsort
#

@njit(parallel=False)
def get_canvas(x_bound, y_bound):
    canvas = zeros(shape=(x_bound, y_bound, 3), dtype=uint8)
    colors = array([randint(128, 256),
                    randint(128, 256),
                    randint(128, 256)])
    for i in prange(x_bound):
        for j in range(y_bound):
            canvas[i, j, 0], \
            canvas[i, j, 1], \
            canvas[i, j, 2] = colors
    return canvas


@njit(parallel=False)
def draw_stroke(canvas, length, x_bound, y_bound):
    x0 = randint(0, x_bound)
    y0 = randint(0, y_bound)
    angle = radians(uniform(0, 360))
    x1 = abs(int(length * cos(angle) + x0))
    y1 = abs(int(length * sin(angle) + y0))
    # don't care about the angle yet
    fill = array([randint(255),
                  randint(255),
                  randint(255)])
    alpha = uniform(0.3, 1)
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    # print('Actual length is {}'.format(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** (1/2)))
    for i, j in zip(range(x0, min(x1 + 1, x_bound)), range(y0, min(y1 + 1, y_bound))):
        canvas[i, j] = fill * alpha + canvas[i, j] * (1 - alpha)
    return canvas
