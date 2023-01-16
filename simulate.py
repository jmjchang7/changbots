import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import math
import random

amplitude_BL = numpy.pi/3.5
frequency_BL = 15
phaseOffset_BL = 0

amplitude_FL = numpy.pi/4
frequency_FL = 15
phaseOffset_FL = numpy.pi/4

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

angles = numpy.linspace(0, numpy.pi*2, 1000)
targetAngles_FL = amplitude_FL * numpy.sin(frequency_FL * angles + phaseOffset_FL)
targetAngles_BL = amplitude_BL * numpy.sin(frequency_BL * angles + phaseOffset_BL)
numpy.save('data/targetAngles_FL.npy', targetAngles_FL)
numpy.save('data/targetAngles_BL.npy', targetAngles_BL)

for i in range(1000):
    time.sleep(1/60)
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_BackLeg', controlMode = p.POSITION_CONTROL, 
                                targetPosition = targetAngles_FL[i], maxForce = 500)
    pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = b'Torso_FrontLeg', controlMode = p.POSITION_CONTROL, 
                                targetPosition = targetAngles_BL[i], maxForce = 500)
    numpy.save('data/backLegSensorValues.npy', backLegSensorValues)
    numpy.save('data/frontLegSensorValues.npy', frontLegSensorValues)
p.disconnect()

# print(backLegSensorValues)
# print(frontLegSensorValues)
