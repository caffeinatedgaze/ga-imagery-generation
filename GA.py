from chromosome import Chromosome
from numpy.random import randint
import cfg
import copy


def crossingover():
    sort_by_fittest()
    pass


def mutation():
    sort_by_fittest()
    pass


def gen_init_pop():
    cfg.population = [Chromosome(cfg.n_strokes) for _ in range(cfg.pop_size - 1)]


def elitism():
    sort_by_fittest()
    cfg.next_pop.append(copy.deepcopy(cfg.population[0]))


def euclide(im):
    if cfg.orig.size != im.size:
        raise Exception('Images should be of equal size\n{} and the one being generated are not'.
                        format(cfg.orig.filename))
    width, height = cfg.orig.size
    distance = 0

    for x in range(width):
        for y in range(height):
            r1, g1, b1 = cfg.orig.getpixel((x, y))
            r2, g2, b2, _ = im.getpixel((x, y))
            distance += abs((r1 + g1 + b1) - (r2 + g2 + b2)) // 3
    return distance


def final_touches():
    sort_by_fittest()
    if cfg.population[0].fitness > cfg.next_pop[0].fitness:
        cfg.population[0] = copy.deepcopy(cfg.next_pop[0])
        # cfg.next_pop = []
        # break
    cfg.next_pop = []


def update_pop_fitness():
    for ch in cfg.population:
        ch.fitness = euclide(ch.generate())


def sort_by_fittest():
    update_pop_fitness()
    cfg.population.sort(key=lambda x: x.fitness)


def print_all_fitness():
    print([x.fitness for x in cfg.population])
