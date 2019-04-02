from time import time
from numpy.random import seed
from matplotlib import pyplot

from GA import *

# import cfg

start = time()

# seed()
gen_init_pop()
update_pop_fitness()
sort_by_fittest()

print('First population fitnesses', end='\t')
print_fitnesses()

cfg.population[0].generate().save('tmp/' + 'init_strokes.png', 'PNG')

init_min_fit = min(cfg.population, key=lambda x: x.fitness).fitness
best_outputs = []
second_outputs = []

for i in range(8196):

    print('%.6d - %.6f seconds' % (i, (time() - start)), end='\t\t')
    best_outputs.append(cfg.population[0].fitness)
    second_outputs.append(cfg.population[1].fitness)
    print('Best two - {}\t{}'.format(cfg.population[0].fitness,
                                     cfg.population[1].fitness))

    elitism()
    # print('Next pop is ', cfg.next_pop[0].fitness)
    crossingover()
    mutation()

    if i % 5 == 0:
        cfg.next_pop[0].generate().save('tmp/' + 'cur_strokes' + '.png', 'PNG')
        # cfg.next_pop[0].generate().save('tmp/' + 'strokes' + str(i) + '.png', 'PNG')

    final_touches()
    # print('')

# print(); print_fitnesses()
# print([x.fitness for x in cfg.population])
# print([x.generate().save('tmp/' + str(x), 'PNG') for x in cfg.population])


update_pop_fitness()
sort_by_fittest()
# cfg.population[0].generate().save('tmp/' + 'strokes.png', 'PNG')

pyplot.plot(best_outputs)
pyplot.xlabel("Iteration")
pyplot.ylabel("Fitness = euclide distance b\w pictures")
pyplot.show()

print('Total  - %.6f seconds' % (time() - start), end='\t\t')
print('Delta fitness -\t{}'.format(init_min_fit - min(cfg.population, key=lambda x: x.fitness).fitness))
