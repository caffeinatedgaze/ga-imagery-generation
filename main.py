from matplotlib import pyplot
from datetime import datetime
from time import time
from GA import *
import json
import cfg

start = time()

gen_init_pop()
sort_by_fittest()

init_min_fit = get_fittest()[1].fitness
best_outputs = []
second_outputs = []

print('First population fitness', get_all_fitness())
print('First population fitness', get_all_types())

# for i in range(cfg.pop_size):
#     cfg.population[i].execute().save('tmp/init_pop/' + 'program_' +
#                                      str(cfg.population[i].fitness) + '.png', 'PNG')

for i in range(4096):  # 2 ** 16 = 65536

    elitism()
    sort_by_fittest()
    best_outputs.append(cfg.population[0].fitness)
    second_outputs.append(cfg.population[1].fitness)

    print('%.6d - %.6f seconds' % (i, (time() - start)), end='\t\t')
    print('Best two - {}\t{}\t{}'.format(cfg.population[0].fitness,
                                         cfg.population[1].fitness,
                                         cfg.population[2].fitness), end='\t\t')
    print('Delta fitness -\t{}'.format(init_min_fit - get_fittest()[1].fitness))

    # print(get_all_fitness())
    crossover()
    mutation()

prime = get_fittest()[1]
prime.execute().save('tmp/' + 'final_' + '.png', 'PNG')

data = dict()
data['date'] = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
data['type'] = prime.type
data['n_quads'] = prime.n
data['fitness'] = prime.fitness
data['program'] = prime.program

json.dump(data, open('library/' + str(data['fitness']) + '___' + data['date'], 'w'))

pyplot.plot(best_outputs)
pyplot.plot(second_outputs)
pyplot.xlabel("Iteration")
pyplot.ylabel("Fitness = euclide distance b\\w pictures")
pyplot.savefig('tmp/analyse' + data['date'] + '.jpg')
pyplot.show()

elitism()
print('Total - %.6f seconds' % (time() - start), end='\t\t')
print('Final delta -\t{}'.format(init_min_fit - get_fittest()[1].fitness))
