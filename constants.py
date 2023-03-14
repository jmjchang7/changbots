import numpy
import random

runTime = 4000

# amplitude_BL = numpy.pi/4
# frequency_BL = 50
# phaseOffset_BL = numpy.pi/4

# amplitude_FL = 4
# frequency_FL = 50
# phaseOffset_FL = numpy.pi/2

numSeeds = 1

amplitude = numpy.pi/4
frequency = 10
phaseOffset = 0.2

numberOfGenerations = 1
populationSize = 1

numLinks = random.randint(2, 5)
numJoints = numLinks - 1

numSensorNeurons = random.randint(1, numLinks-1)

SensorIndexList = [1]*numSensorNeurons + [0]*(numLinks-numSensorNeurons)
random.shuffle(SensorIndexList)

numMotorNeurons = numJoints

motorJointRange = 0.6