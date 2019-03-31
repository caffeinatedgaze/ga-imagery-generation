import cfg
from time import time
from GA import *

start = time()

gen_init_pop()

for i in range(256):
    cal_pop_fitness()
    elitism()
    cfg.next_pop[0].generate().save('tmp/' + 'strokes' + str(i) + '.png', 'PNG')
    crossingover()
    mutation()
    final_touches()
    print('%.6d - %.6f seconds' % (i, (time() - start)))

elitism()
cfg.next_pop[0].generate().save('tmp/' + 'strokes.png', 'PNG')

print('%.6f seconds' % (time() - start))
