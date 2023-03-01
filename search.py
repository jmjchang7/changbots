import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import random
import constants as c
import matplotlib.pyplot as plt

fitnessCurves = [[] for _ in range(c.numSeeds)]

for i in range(1, c.numSeeds + 1):
    phc = PARALLEL_HILL_CLIMBER()
    phc.Evolve()
    phc.Show_Best()
    fitnessCurves[i-1] = phc.Get_Fitness_Curve()

# plot all curves
for i in range(c.numSeeds):
    plt.plot(range(c.numberOfGenerations+1), fitnessCurves[i], label='Seed ' + str(i + 1))

plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.title('Evolution Curves')

plt.legend()
plt.show()