from numpy.random import randint, choice
from chromosome import Chromosome
from copy import deepcopy
import cfg


#
# 1. Accelerated convergence in mutation
# 2. Fitness write threshold
# 3. The optimal number of pr. in a population is 4
# 4. Midori Kuma
#

def crossover():
    distribution = [0.3, 0.3, 0.2, 0.2]
    indices = choice(cfg.pop_size, 2, replace=False, p=distribution)
    ch_1 = deepcopy(cfg.population[indices[0]])
    ch_2 = deepcopy(cfg.population[indices[1]])

    prior_1 = ch_1.fitness
    prior_2 = ch_2.fitness

    point = cfg.pop_size // 2
    ch_1.program[:point], ch_2.program[:point] = ch_2.program[:point], ch_1.program[:point]
    # check if fitness has changed to the better

    update_fitness(ch_1)
    if prior_1 > ch_1.fitness:
        cfg.population[indices[0]] = ch_1

    update_fitness(ch_2)
    if prior_2 > ch_2.fitness:
        cfg.population[indices[1]] = ch_2

    sort_by_fittest()


def mutation():
    distribution = [0.3, 0.3, 0.3, 0.1]
    indices = choice(cfg.pop_size, 1, replace=False, p=distribution)
    ch = deepcopy(cfg.population[indices[0]])

    point = randint(cfg.n_quads - 1)

    prior = ch.fitness

    for i in range(0, point):
        ch.program[i] = Chromosome.get_quad_uniform(cfg.length, (0, cfg.x_bound), (0, cfg.y_bound))

    update_fitness(ch)
    if prior > ch.fitness:
        cfg.population[indices[0]] = ch

    sort_by_fittest()


def elitism():
    ind_fittest = get_fittest()[0]
    if cfg.prime:
        if cfg.prime.fitness < cfg.population[ind_fittest].fitness:
            cfg.population[ind_fittest] = deepcopy(cfg.prime)
            # we want the prime to stay the same, jic # cfg.prime = None
        elif cfg.prime.fitness != cfg.population[ind_fittest].fitness:
            cfg.prime = deepcopy(cfg.population[ind_fittest])
            cfg.prime.execute().save('tmp/' + 'prime_' +
                                     str(cfg.prime.fitness) + '.png', 'PNG')
            # fitness write threshold; save when it's better
    else:
        print('Best ch is - ', cfg.population[ind_fittest].fitness)
        cfg.prime = deepcopy(cfg.population[ind_fittest])


def gen_init_pop():
    cfg.population = [Chromosome(cfg.n_quads) for _ in range(cfg.pop_size)]


def get_fittest():
    return min(enumerate(cfg.population), key=lambda x: x[1].fitness)


def sort_by_fittest():
    update_pop_fitness()
    cfg.population.sort(key=lambda x: x.fitness)


def update_pop_fitness():
    for ch in cfg.population:
        update_fitness(ch)


def update_fitness(ch):
    ch.fitness = euclide(ch.execute())


def euclide(im):
    if cfg.orig.size != im.size:
        raise Exception('Images should be of equal size\n{} and the one being executed are not'.
                        format(cfg.orig.filename))
    width, height = cfg.orig.size
    distance = 0
    for x in range(width):
        for y in range(height):
            r1, g1, b1 = cfg.orig.getpixel((x, y))
            r2, g2, b2, _ = im.getpixel((x, y))
            distance += abs((r1 + g1 + b1) - (r2 + g2 + b2)) // 3
    return distance


def get_all_fitness():
    return [x.fitness for x in cfg.population]


def get_all_types():
    return [x.type for x in cfg.population]
