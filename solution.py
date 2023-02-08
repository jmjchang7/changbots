import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.weights = numpy.random.rand(c.numSensorNeurons, c.numMotorNeurons) * 2 - 1
        self.myID = nextAvailableID

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Send_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        fitnessFile = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("rm fitness" + str(self.myID) + ".txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Runway", pos=[-2,-2,4], size=[40,4,8])
        pyrosim.End()

    def Create_Body(self):

        x,y,z = -2,-2,8

        pyrosim.Start_URDF("body.urdf")
        # absolute
        pyrosim.Send_Cube(name = "Torso", pos=[0+x,0+y,1+z], size=[1,1,1])
        # absolute
        pyrosim.Send_Joint(name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0+x,-0.5+y,1+z], jointAxis = "1 0 0")
        # relative
        pyrosim.Send_Cube(name = "BackLeg", pos=[0,-0.5,0], size=[0.2,1,0.2])
        # absolute
        pyrosim.Send_Joint(name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0+x,0.5+y,1+z], jointAxis = "1 0 0")
        #relative
        pyrosim.Send_Cube(name = "FrontLeg", pos=[0,0.5,0], size=[0.2,1,0.2])
        #absolute, changed leftleg joint to first leftleg joint
        pyrosim.Send_Joint(name = "Torso_LeftLeg1" , parent= "Torso" , child = "LeftLeg1" , type = "revolute", position = [-0.5+x,0.5+y,1+z], jointAxis = "0 1 0")
        #relative, changed left leg to LeftLeg1
        pyrosim.Send_Cube(name = "LeftLeg1", pos=[-0.5,0,0], size=[1,0.2,0.2])
        #absolute, added second left leg joint
        pyrosim.Send_Joint(name = "Torso_LeftLeg2" , parent= "Torso" , child = "LeftLeg2" , type = "revolute", position = [-0.5+x,-0.5+y,1+z], jointAxis = "0 1 0")
        #relative, added second joint
        pyrosim.Send_Cube(name = "LeftLeg2", pos=[-0.5,0,0], size=[1,0.2,0.2])
        #absolute
        pyrosim.Send_Joint(name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5+x,0+y,1+z], jointAxis = "0 1 0")
        # all relative
        pyrosim.Send_Cube(name = "RightLeg", pos=[0.5,0,0], size=[1,0.2,0.2])
        pyrosim.Send_Joint(name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg" , child = "FrontLowerLeg" , type = "revolute", position = [0,1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name = "FrontLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
        pyrosim.Send_Joint(name = "BackLeg_BackLowerLeg" , parent= "BackLeg" , child = "BackLowerLeg" , type = "revolute", position = [0,-1,0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name = "BackLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
        pyrosim.Send_Joint(name = "LeftLeg1_LeftLowerLeg1" , parent= "LeftLeg1" , child = "LeftLowerLeg1" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name = "LeftLowerLeg1", pos=[0,0,-0.5], size=[0.2,0.2,1])
        # added second left leg to left lowerleg
        pyrosim.Send_Joint(name = "LeftLeg2_LeftLowerLeg2" , parent= "LeftLeg2" , child = "LeftLowerLeg2" , type = "revolute", position = [-1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name = "LeftLowerLeg2", pos=[0,0,-0.5], size=[0.2,0.2,1])
        pyrosim.Send_Joint(name = "RightLeg_RightLowerLeg" , parent= "RightLeg" , child = "RightLowerLeg" , type = "revolute", position = [1,0,0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name = "RightLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
        pyrosim.End()

    def Send_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "RightLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "LeftLeg1")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "LeftLeg2")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg1")
        # added
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg2")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 9 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10 , jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 11 , jointName = "Torso_RightLeg")
        pyrosim.Send_Motor_Neuron( name = 12 , jointName = "Torso_LeftLeg1")
        pyrosim.Send_Motor_Neuron( name = 13 , jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 14 , jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "LeftLeg1_LeftLowerLeg1")
        #added
        pyrosim.Send_Motor_Neuron( name = 15 , jointName = "LeftLeg2_LeftLowerLeg2")
        pyrosim.Send_Motor_Neuron( name = 16 , jointName = "RightLeg_RightLowerLeg")
        
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)

        self.weights[randomRow,randomColumn] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID