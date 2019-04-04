from time import time
from matplotlib import pyplot
from GA import *
import cfg

start = time()

gen_init_pop()
sort_by_fittest()

init_min_fit = min(cfg.population, key=lambda x: x.fitness).fitness
best_outputs = []
second_outputs = []

print('First population fitness', get_all_fitness())
print('First population fitness', get_all_types())

for i in range(cfg.pop_size - 1):
    cfg.population[i].execute().save('init_pop/' + 'program_' +
                                     str(cfg.population[i].fitness) + '.png', 'PNG')

for i in range(1024):
    print('%.6d - %.6f seconds' % (i, (time() - start)), end='\t\t')
    print('Best two - {}\t{}'.format(cfg.population[0].fitness,
                                     cfg.population[1].fitness), end='\t\t')
    print('Delta fitness -\t{}'.format(init_min_fit - min(cfg.population, key=lambda x: x.fitness).fitness))
    best_outputs.append(cfg.population[0].fitness)
    second_outputs.append(cfg.population[1].fitness)

    elitism()
    crossover()
    mutation()

pyplot.plot(best_outputs)
pyplot.plot(second_outputs)
pyplot.xlabel("Iteration")
pyplot.ylabel("Fitness = euclide distance b\\w pictures")
pyplot.show()

print('Total - %.6f seconds' % (time() - start), end='\t\t')
print('Final delta -\t{}'.format(init_min_fit - min(cfg.population, key=lambda x: x.fitness).fitness))
