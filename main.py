from time import time
from GA import *

start = time()

gen_init_pop()
cal_pop_fitness()
elitism()
crossingover()
mutation()
final_touches()

elitism()
next_pop[0].generate().save('tmp/' + 'strokes.png', 'PNG')

print('%.6f seconds' % (time() - start))
