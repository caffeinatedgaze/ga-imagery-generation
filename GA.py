from chromosome import Chromosome
from random import randint
from PIL import Image

orig       = Image.open('src/tree_lossy.jpg')
im_size    = orig.size
n_strokes  = 1024
pop_size   = 5
population = []
next_pop   = []
fitness    = []


def set_params(canonical_im, size, p_size=3, n_strks=1024):
    global orig, pop_size, n_strokes, fitness, next_pop, im_size
    orig = canonical_im
    im_size = size
    pop_size = p_size
    n_strokes = n_strks
    next_pop = []


def gen_init_pop():
    global population, pop_size, n_strokes, im_size
    population = [Chromosome(n_strokes, im_size) for _ in range(pop_size)]


def cal_pop_fitness():
    global fitness
    fitness = [euclide(x.generate()) for x in population]


def elitism():
    global population, next_pop
    best_ind = min(enumerate(fitness), key=lambda x: x[1])[0]
    next_pop.append(population[best_ind])
    population.remove(population[best_ind])


def crossingover():
    ind_1, ind_2 = randint(0, len(population) - 1), randint(0, len(population) - 1)

    strokes_1 = population[ind_1].strokes
    strokes_2 = population[ind_2].strokes
    cross_point = len(strokes_1) // 2

    for i in range(0, cross_point):
        strokes_1[i], strokes_2[i] = strokes_2[i], strokes_1[i]

    population[ind_1].strokes = strokes_1
    population[ind_2].strokes = strokes_2


def euclide(im):
    global orig
    if orig.size != im.size:
        raise Exception('Images should be of equal size\n{} and the one being generated are not'.
                        format(orig.filename))
    width, height = orig.size
    distance = 0

    for x in range(width):
        for y in range(height // 2 - height // 4, height - height // 4):
            r1, g1, b1 = orig.getpixel((x, y))
            r2, g2, b2, _ = im.getpixel((x, y))
            distance += ((r1 + g1 + b1) - (r2 + g2 + b2)) ** 2
    return distance


def mutation():
    ind = randint(len(population) // 2, len(population) - 1)
    for i in range(len(population) // 2 - 1, ind):
        strokes = population[ind].strokes
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke()
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke()
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke()
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke()
        population[ind].strokes = strokes


def final_touches():
    global population, next_pop
    population += next_pop
    next_pop = []
