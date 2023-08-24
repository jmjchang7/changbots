import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName

        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.offset = c.phaseOffset

        self.motorValues = numpy.linspace(self.offset, 2 * numpy.pi * self.frequency, 1000)
        self.motorValues = numpy.sin(self.motorValues) * self.amplitude

    def Set_Value(self, robotId, desiredAngle):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, 
                        targetPosition = desiredAngle, maxForce = 50)