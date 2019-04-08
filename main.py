from gen_gif import npy_list_sorted
from numpy import save, load
from time import time
from genetic import *
from PIL import Image
import cfg

input('Press any button')

start = time()

cfg.new_population = gen_population(cfg.pop_size, (cfg.x_bound, cfg.y_bound))

if npy_list_sorted():
    cfg.new_population[0] = load('library/' + npy_list_sorted()[::-1][0])

cfg.fitness = cal_pop_fitness(cfg.new_population, cfg.target)
init_min_fitness = min(cfg.fitness)

Image.fromarray(get_best()).save('tmp/' + 'strokes' + '.png', 'PNG')

chkpoint_fit = 0
for i in range(2 ** 64):
    cfg.fitness = cal_pop_fitness(cfg.new_population, cfg.target)
    parents = select_mating_pool(cfg.new_population, cfg.fitness, cfg.mating_size)
    cfg.offspring_crossover = crossover(parents, cfg.mating_size, (cfg.x_bound, cfg.y_bound),
                                        cfg.crossover_size)

    cfg.offspring_mutation = mutation(cfg.offspring_crossover, (cfg.x_bound, cfg.y_bound),
                                      cfg.crossover_size, cfg.length)

    cfg.new_population[0:parents.shape[0], :] = parents
    cfg.new_population[parents.shape[0]:, :] = cfg.offspring_mutation

    print('%.6d - %.6f seconds' % (i, (time() - start)), end='\t\t')
    print('Delta fitness -\t{}'.format(init_min_fitness - min(cfg.fitness)))

    if i % 250 == 0:
        save('library/_data__' + str(i), get_best())
    if abs(chkpoint_fit - min(cfg.fitness)) >= 10000:
        chkpoint_fit = min(cfg.fitness)
        # Image.fromarray(get_best()).save('tmp/' + 'strokes' + '.png', 'PNG')
        Image.fromarray(get_best()).save('tmp/' + 'strokes' + '.jpg', 'JPEG')
        save('library/_data__' + str(i), get_best())

print('Total - %.6f seconds' % (time() - start), end='\t\t')
print('Delta fitness -\t{}'.format(min(cfg.fitness) - init_min_fitness))

# 568974
# 1470144
# 1578020
# 1602491
# 1625416
