from chromosome import Chromosome
from random import randint
import cfg


# def set_params(canonical_im, size, p_size=3, n_strks=1024):
#     # global cfg.orig, pop_size, n_strokes, fitness, cfg.next_pop, im_size
#     cfg.orig = canonical_im
#     im_size = size
#     pop_size = p_size
#     n_strokes = n_strks
#     cfg.next_pop = []


def gen_init_pop():
    cfg.population = [Chromosome(cfg.n_strokes, cfg.im_size, cfg.length) for _ in range(cfg.pop_size)]


def cal_pop_fitness():
    global fitness
    fitness = [euclide(x.generate()) for x in cfg.population]


def elitism():
    best_ind = min(enumerate(fitness), key=lambda x: x[1])[0]
    cfg.next_pop.append(cfg.population[best_ind])
    cfg.population.remove(cfg.population[best_ind])


def crossingover():
    ind_1, ind_2 = randint(0, len(cfg.population) - 1), randint(0, len(cfg.population) - 1)
    strokes_1 = cfg.population[ind_1].strokes
    strokes_2 = cfg.population[ind_2].strokes
    cross_point = len(strokes_1) // 2

    for i in range(0, cross_point):
        strokes_1[i], strokes_2[i] = strokes_2[i], strokes_1[i]

    cfg.population[ind_1].strokes = strokes_1
    cfg.population[ind_2].strokes = strokes_2


def euclide(im):
    if cfg.orig.size != im.size:
        raise Exception('Images should be of equal size\n{} and the one being generated are not'.
                        format(cfg.orig.filename))
    width, height = cfg.orig.size
    distance = 0

    for x in range(width):
        for y in range(height // 2 - height // 4, height - height // 4):
            r1, g1, b1 = cfg.orig.getpixel((x, y))
            r2, g2, b2, _ = im.getpixel((x, y))
            distance += ((r1 + g1 + b1) - (r2 + g2 + b2)) ** 2
    return distance


def mutation():
    ind = randint(len(cfg.population) // 2, len(cfg.population) - 1)
    for i in range(len(cfg.population) // 2 - 1, ind):
        strokes = cfg.population[ind].strokes
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke(cfg.length)
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke(cfg.length)
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke(cfg.length)
        strokes[randint(0, len(strokes) - 1)] = Chromosome.get_stroke(cfg.length)
        cfg.population[ind].strokes = strokes


def final_touches():
    cfg.population += cfg.next_pop
    cfg.next_pop = []
