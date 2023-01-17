import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.amplitude_BL

        if self.jointName == b'Torso_BackLeg':
            self.frequency = c.frequency_BL
        else:
            self.frequency = c.frequency_BL/2

        self.offset = c.phaseOffset_BL
        self.motorValues = self.amplitude * numpy.sin(self.frequency * numpy.linspace(0, numpy.pi*2, 1000) + self.offset)  

    def Set_Value(self, robotId, t):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, 
                        targetPosition = self.motorValues[t], maxForce = 500)

    def Save_Values(self):
        numpy.save('data/motorcommands.npy', self.motorValues)