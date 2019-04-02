from chromosome import Chromosome
from numpy.random import randint
import cfg
import copy


def gen_init_pop():
    cfg.population = [Chromosome(cfg.n_strokes,
                      Chromosome.get_stroke_normal if randint(0, 10) >= 3 else \
                      Chromosome.get_stroke_uniform) \
                      for _ in range(cfg.pop_size - 1)]


def elitism():
    sort_by_fittest()
    cfg.next_pop.append(copy.deepcopy(cfg.population[0]))


def crossingover():
    sort_by_fittest()
    probability = 3

    if randint(0, 10) <= probability:
        ind_1 = 0
    else:
        ind_1 = randint(0, len(cfg.population) - 1)

    if randint(0, 10) <= probability:
        ind_2 = 1
    else:
        ind_2 = ind_1 + randint(0, len(cfg.population) - ind_1 - 1)

    # ind_1, ind_2 = min(ind_1, ind_2), max(ind_1, ind_2)

    print('Indices are - {} and {}'.format(ind_1, ind_2))

    strokes_1 = cfg.population[ind_1].strokes
    strokes_2 = cfg.population[ind_2].strokes
    cross_point_1 = randint(0, len(strokes_1) - 1)
    cross_point_2 = randint(0, len(strokes_1) - 1)

    for i in range(min(cross_point_1, cross_point_2), max(cross_point_1, cross_point_2)):
        strokes_1[i], strokes_2[i] = strokes_2[i], strokes_1[i]

    if ind_1 == 0 or ind_1 == 1:
        if randint(0, 10) == 3:
            cfg.population[ind_1].strokes = strokes_1
            cfg.population[ind_2].strokes = strokes_2
        else:
            cfg.population[ind_2].strokes = strokes_2

    if ind_2 == 0 or ind_2 == 1:
        if randint(0, 10) == 3:
            cfg.population[ind_1].strokes = strokes_1
            cfg.population[ind_2].strokes = strokes_2
        else:
            cfg.population[ind_1].strokes = strokes_1


def mutation():
    probability = 7
    sort_by_fittest()

    if randint(0, 10) <= probability:
        if randint(0, 1) == 1:
            ind_1 = 0
        else:
            ind_1 = 1
    else:
        ind_1 = randint(0, len(cfg.population) - 1)

        # if randint(0, 10) <= probability:
        #     ind_2 = 1
        # else:
        #     ind_2 = ind_1 + randint(0, len(cfg.population) - ind_1 - 1)

        # for i in range(ind_1, ind_2):
        # print('Flag A ', ind_1)
        strokes = cfg.population[ind_1].strokes
        first = randint(0, len(strokes) // 4)
        second = first + randint(len(strokes) // 4, 3 * len(strokes) // 4 - 1)
        for j in range(first, second):
            strokes[j] = Chromosome.get_stroke_uniform(cfg.length)

        cfg.population[ind_1].strokes = strokes


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
    # print('After GA, the best is {}, was {}'.format(cfg.population[0].fitness,
    #                                                 cfg.next_pop[0].fitness))
    # for i in range(len(cfg.population)):
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


def print_fitnesses():
    print([x.fitness for x in cfg.population])
