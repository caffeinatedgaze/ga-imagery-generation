from chromosome import Chromosome
import copy
import cfg


#
# 1. Accelerated convergence in mutation
# 2. Fitness write threshold
# 3. The optimal number of pr. in a population is 4
# 4. Midori Kuma
#

def crossover():
    sort_by_fittest()
    pass


def mutation():
    sort_by_fittest()
    pass


def elitism():
    ind_fittest = get_fittest()[0]
    if cfg.prime and cfg.prime.fitness < cfg.population[ind_fittest].fitness:
        cfg.population[ind_fittest] = copy.deepcopy(cfg.prime)
        # we want the prime to stay the same, jic # cfg.prime = None
    else:
        print('Best ch is - ', cfg.population[ind_fittest].fitness)
        cfg.prime = copy.deepcopy(cfg.population[ind_fittest])


def gen_init_pop():
    cfg.population = [Chromosome(cfg.n_quads) for _ in range(cfg.pop_size)]


def get_fittest():
    return min(enumerate(cfg.population), key=lambda x: x[1].fitness)


def sort_by_fittest():
    update_pop_fitness()
    cfg.population.sort(key=lambda x: x.fitness)


def update_pop_fitness():
    for ch in cfg.population:
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
