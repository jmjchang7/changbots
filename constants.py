import numpy
import random

amplitude_BL = numpy.pi/4
frequency_BL = 50
phaseOffset_BL = numpy.pi/4

amplitude_FL = 4
frequency_FL = 50
phaseOffset_FL = 0

numberOfGenerations = 1
populationSize = 1

numLinks = 8
numJoints = 7

numSensorNeurons = random.randint(1, numLinks-1)

SensorIndexList = [1]*numSensorNeurons + [0]*(numLinks-numSensorNeurons)
random.shuffle(SensorIndexList)

numMotorNeurons = numJoints

motorJointRange = 0.5