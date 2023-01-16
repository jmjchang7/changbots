import numpy
import matplotlib.pyplot

backLegSensorValues = numpy.load('data/backLegSensorValues.npy')
# print(backLegSensorValues)

frontLegSensorValues = numpy.load('data/frontLegSensorValues.npy')
# print(frontLegSensorValues)

targetAngles_FL = numpy.load('data/targetAngles_FL.npy')
targetAngles_BL = numpy.load('data/targetAngles_BL.npy')
matplotlib.pyplot.plot(targetAngles_BL, label = 'backLeg Target Angles', linewidth =2)
matplotlib.pyplot.plot(targetAngles_FL, label = 'frontLeg Target Angles')

# matplotlib.pyplot.plot(backLegSensorValues, label = 'backLegSensor', linewidth = 2)
# matplotlib.pyplot.plot(frontLegSensorValues, label = 'frontLegSensor')
matplotlib.pyplot.xlabel('Steps')
matplotlib.pyplot.ylabel('Value in radians')
matplotlib.pyplot.title('Motor Commands')
matplotlib.pyplot.legend()
matplotlib.pyplot.show()