import numpy
import random

runTime = 1000

# amplitude_BL = numpy.pi/4
# frequency_BL = 50
# phaseOffset_BL = numpy.pi/4

# amplitude_FL = 4
# frequency_FL = 50
# phaseOffset_FL = numpy.pi/2

amplitude = numpy.pi/8
frequency = 50
phaseOffset = 0

numberOfGenerations = 5
populationSize = 5

numLinks = random.randint(3, 5)
numJoints = numLinks - 1

numSensorNeurons = random.randint(1, numLinks-1)

SensorIndexList = [1]*numSensorNeurons + [0]*(numLinks-numSensorNeurons)
random.shuffle(SensorIndexList)

numMotorNeurons = numJoints

motorJointRange = 1