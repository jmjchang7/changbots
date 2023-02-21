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
        pyrosim.Send_Cube(name="Block", pos=[-2,-2,0.5], size=[1,1,1])
        pyrosim.End()

    def Create_Body(self):

        # initialize variables
        startX,startY,startZ = 0,0,0
        self.dimensionsList = [] #list of lists that holds dimensions for each cube in order. For example, 0 index is [x dim, y dim, z dim]
        self.positionsList = [] #list of ([position list], "Name") that holds positions and name of each cube AND link in order. 
        self.armList = [0] * c.numLinks # list of hwo many arms each snake link has
        for i in c.numLinks:
            self.armList[i] = random.randint(0, 2)
        
        
        # make dimensions and positions of each randomized link + its respective joint
        linkCount = 0
        for linkN in range(c.numLinks):
            sizeX = random.random()*1.4 + 1
            sizeY = random.random()*0.7 + 1
            sizeZ = random.random()*1.1 + 1
            self.dimensionsList.append([sizeX, sizeY, sizeZ])

            if linkN == 0:
                startZ = sizeZ/2
                self.positionsList.append([[startX, startY, startZ], "Link" + str(linkCount)]) # first link
                self.positionsList.append([[sizeX/2, startY, startZ], "Link" + str(linkCount) + "_Link" + str(linkCount + 1)]) # first joint
                linkCount += 1
            elif linkN < (c.numLinks - 1):
                self.positionsList.append([[sizeX/2, 0, 0], "Link" + str(linkCount)]) #next link

                if self.armList[linkN] == 0:
                    pass
                elif self.armList[linkN] == 1:
                    pass
                else:
                    pass

                # MAKE 0, 1, or 2 ARMS
                    # For each arm:
                        # Attach one or two legs

                self.positionsList.append([[sizeX, 0, 0], "Link" + str(linkCount) + "_Link" + str(linkCount + 1)]) #next joint
                linkCount += 1
            elif linkN == (c.numLinks - 1):
                self.positionsList.append([[sizeX/2, 0, 0], "Link" + str(linkCount)]) #last link (has no next joint)

        # now actually make the "Cubes" and "Joints"
        for linkN in range(c.numLinks-1):
            pyrosim.Start_URDF("body.urdf")
            currentLink = 0
            for positionI in self.positionsList:
                if "_" not in positionI[1]:
                    if c.SensorIndexList[currentLink] == 1: # if sensor, set green
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.dimensionsList[currentLink], color_string = '    <color rgba= "0 255.0 0.0 1.0"/>', color = 'Green')
                    else:
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.dimensionsList[currentLink])
                    currentLink += 1
                else:
                    pyrosim.Send_Joint(name = positionI[1] , parent= positionI[1].split('_')[0] , child = positionI[1].split('_')[1] , type = "revolute", position = positionI[0], jointAxis = "0 0 1")
            linkCount = 0

        pyrosim.End()

    def Send_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # send sensor and motor neurons
        neuronCount = 0
        currentLink = 0
        for positionI in self.positionsList:
                if "_" not in positionI[1]: # checks if it's a Link
                    if c.SensorIndexList[currentLink] == 1: #check if it should be a sensor
                        pyrosim.Send_Sensor_Neuron(name = neuronCount, linkName = positionI[1])
                        neuronCount += 1
                    currentLink += 1
        for positionI in self.positionsList:
                if "_" in positionI[1]: # checks if it's a Joint
                    pyrosim.Send_Motor_Neuron( name = neuronCount, jointName = positionI[1])
                    neuronCount += 1
        
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