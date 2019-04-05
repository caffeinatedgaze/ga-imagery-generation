from time import time
from genetic import *
from PIL import Image
import cfg

start = time()

cfg.new_population = gen_population(cfg.pop_size, (cfg.x_bound, cfg.y_bound))

# for x in cfg.new_population:
#     Image.fromarray(x).show()

cfg.fitness = cal_pop_fitness(cfg.new_population, cfg.target)
init_min_fitness = min(cfg.fitness)

Image.fromarray(get_best()[0]).save('tmp/' + 'strokes' + '.jpeg', 'JPEG')

for i in range(2 ** 16):
    cfg.fitness = cal_pop_fitness(cfg.new_population, cfg.target)
    # print(cfg.new_population[0].shape)
    parents = select_mating_pool(cfg.new_population, cfg.fitness, cfg.mating_size)
    cfg.offspring_crossover = crossover(parents, cfg.mating_size, (cfg.x_bound, cfg.y_bound),
                                        cfg.crossover_size)

    cfg.offspring_mutation = mutation(cfg.offspring_crossover, (cfg.x_bound, cfg.y_bound),
                                      cfg.crossover_size, cfg.length)

    cfg.new_population[0:parents.shape[0], :] = parents
    cfg.new_population[parents.shape[0]:, :] = cfg.offspring_mutation

    print('%.6d - %.6f seconds' % (i, (time() - start)), end='\t\t')
    print('Delta fitness -\t{}'.format(min(cfg.fitness) - init_min_fitness))

    if i % 250 == 0:
        print(cfg.fitness)
        print('Best fit = ', get_best())
        Image.fromarray(get_best()).save('tmp/' + 'strokes' + '.jpeg', 'JPEG')

# for i in range(1024):
#     euclide(get_canvas(), cfg.target)

print('Total - %.6f seconds' % (time() - start), end='\t\t')
print('Delta fitness -\t{}'.format(min(cfg.fitness) - init_min_fitness))

# 568974
# 1470144
# 1578020
# 1602491
# 1625416
