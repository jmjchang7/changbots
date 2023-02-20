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
        pyrosim.Start_URDF("body.urdf")
        # body (link0)
        # legs (links 1-4)
        # tail (link5)
        # neck (link6)
        # head (link7)
        # body-leg joints (joints 8-11)
        # body-tail joint (joint 12)
        # body-neck joint (joint 13)
        # neck-head joint (joint 14)

        # holds dimensions for links 0-7     
        self.dimensionsList = [None] * c.numLinks
        # indices in position (and dimension)
        tot_positions = c.numLinks + c.numJoints
        linkInd = 0
        jointInd = c.numLinks
        
        # holds positions for links 0-7, then joints (see readme file for more details diagram)
        # gives total of 8 link positions + 7 joint positions = 15 positions
        self.positions = [None] * tot_positions

        # color/sensor array
        sensorList = []
        for num in range(len(c.SensorIndexList)):
            if c.SensorIndexList[num] == 1:
                sensorList.append(['    <color rgba= "0 255.0 0.0 1.0"/>', 'Green'])
            else:
                sensorList.append(['    <color rgba="0 1.0 1.0 1.0"/>', 'Cyan'])

        print(c.SensorIndexList)

        #########################################################################################

        # BODY
        # Make dimensions
        bodyY = random.random()*2 + 2
        bodyX = random.random()*2 + 2
        body_height = random.random()*2 + 2
        bodyZ = random.random()*2 + 2

        # Add dimensions/position to list
        self.dimensionsList[linkInd] = [bodyX, bodyY, bodyZ]
        body_pos = ([[0, 0, body_height + bodyZ/2], 'Link0'])
        self.positions[linkInd] = body_pos
        startX, startY, startZ = body_pos[0]
        
        # Send pyrosim cube
        pyrosim.Send_Cube(name = body_pos[1], pos=self.positions[linkInd][0], size=self.dimensionsList[linkInd], color_string=sensorList[linkInd][0], color=sensorList[linkInd][1])
        linkInd += 1 # linkInd = 1

        #########################################################################################

        # BODY-LEG JOINTS + LEGS
        # Make dimensions and self.positions
        legY = (random.random()*0.5+0.5) * bodyY/3 # scale leg width by existing body width
        legX = (random.random()*0.5+0.5) * bodyX/4 # scale leg length by existing body length
        legHeight = body_height
        numLegs = 4

        legs_dim = [legX, legY, legHeight]
        leg_joints_pos = [[(startX - bodyX/2 + legX/2), (startY - bodyY/2 + legY/2), legHeight],
                    [(startX + bodyX/2 - legX/2), (startY - bodyY/2 + legY/2), legHeight],
                    [(startX + bodyX/2 - legX/2), (startY + bodyY/2 - legY/2), legHeight],
                    [(startX - bodyX/2 + legX/2), (startY + bodyY/2 - legY/2), legHeight]]

        # (BODY-LEG JOINTS) Add positions to list + Send pyrosim joints
        for i in range(numLegs):
            self.positions[jointInd] = [[leg_joints_pos[i][0], leg_joints_pos[i][1], leg_joints_pos[i][2]], 'Link0_Link' + str(jointInd-c.numJoints)]
            pyrosim.Send_Joint(name = self.positions[jointInd][1], parent= self.positions[jointInd][1].split('_')[0] , child = self.positions[jointInd][1].split('_')[1] , type = "revolute", position = self.positions[jointInd][0], jointAxis = "0 1 0")
            jointInd += 1
        # jointInd = 12            

        # (LEGS) Add dimensions/positions to list + Send pyrosim cubes
        for leg in range(numLegs):
            self.dimensionsList[linkInd] = legs_dim
            self.positions[linkInd] = [[0, 0, -legHeight/2], 'Link' + str(linkInd)]
            pyrosim.Send_Cube(name = self.positions[linkInd][1], pos=self.positions[linkInd][0], size=self.dimensionsList[linkInd], color_string=sensorList[linkInd][0], color=sensorList[linkInd][1])    
            linkInd+=1
        # linkInd = 5
        
        #########################################################################################
        
        # BODY-TAIL JOINT + TAIL LINK
        # (TAIL) Make dimensions/self.positions
        tailY = random.random()*5
        tailX = random.random()*5 + 5
        tailZ = random.random()*5
        tail_joint_pos = [startX + bodyX/2, startY, startZ]

        # (BODY-TAIL JOINT) Add position to list, send pyrosim Joint
        self.positions[jointInd] = [tail_joint_pos, 'Link0_Link' + str(linkInd)]
        pyrosim.Send_Joint(name = self.positions[jointInd][1], parent= self.positions[jointInd][1].split('_')[0] , child = self.positions[jointInd][1].split('_')[1] , type = "revolute", position = self.positions[jointInd][0], jointAxis = "0 0 1")

        # (TAIL) Add dimension to list, send pyrosim Cube
        self.dimensionsList[linkInd] = [tailX, tailY, tailZ]
        self.positions[linkInd] = [[tailX/2, 0, 0], 'Link' + str(linkInd)]
        pyrosim.Send_Cube(name = self.positions[linkInd][1], pos=self.positions[linkInd][0], size=self.dimensionsList[linkInd], color_string=sensorList[linkInd][0], color=sensorList[linkInd][1]) 
        linkInd += 1 # linkInd = 6
        jointInd += 1 # jointInd = 13
         
         #########################################################################################

        # BODY-NECK JOINT + NECK + NECK-HEAD JOINT + HEAD
        # (NECK + HEAD) Make dimensions
        neckX = random.random() + 1
        neckY = random.random() + 1
        neckZ = random.random() + 1
        neck_joint_pos = [startX - bodyX/2 + neckX/2, startY, startZ + bodyZ/2]

        headX = random.random() + 1
        headY = random.random() + 1
        headZ = random.random() + 1
        head_joint_pos = [- neckX/2, 0, headZ/2]

        numNeckJoints = 2 # includes neck-head joint

        for jointNum in range(numNeckJoints):
            if jointNum == 0: #body-neck and neck
                self.positions[jointInd] = [neck_joint_pos, 'Link0_Link' + str(linkInd)]
                pyrosim.Send_Joint(name = self.positions[jointInd][1], parent= self.positions[jointInd][1].split('_')[0] , child = self.positions[jointInd][1].split('_')[1] , type = "revolute", position = self.positions[jointInd][0], jointAxis = "0 0 1")
                jointInd += 1

                self.dimensionsList[linkInd] = [neckX, neckY, neckZ]
                self.positions[linkInd] = [[0, 0, neckZ/2], 'Link' + str(linkInd)]
                pyrosim.Send_Cube(name = self.positions[linkInd][1], pos=self.positions[linkInd][0], size=self.dimensionsList[linkInd], color_string=sensorList[linkInd][0], color=sensorList[linkInd][1]) 
                linkInd += 1
            else: #neck-head and head
                self.positions[jointInd] = [head_joint_pos, 'Link' + str(linkInd-1) + '_Link' + str(linkInd)]
                pyrosim.Send_Joint(name = self.positions[jointInd][1], parent= self.positions[jointInd][1].split('_')[0] , child = self.positions[jointInd][1].split('_')[1] , type = "revolute", position = self.positions[jointInd][0], jointAxis = "1 0 0")
                jointInd += 1

                self.dimensionsList[linkInd] = [headX, headY, headZ]
                self.positions[linkInd] = [[-headX/2, 0, 0], 'Link' + str(linkInd)]
                pyrosim.Send_Cube(name = self.positions[linkInd][1], pos=self.positions[linkInd][0], size=self.dimensionsList[linkInd], color_string=sensorList[linkInd][0], color=sensorList[linkInd][1]) 
                linkInd += 1

        # jointInd = 15
        # linkInd = 8
        pyrosim.End()

    def Send_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # send sensor and motor neurons
        neuronCount = 0
        currentLink = 0
        for positionI in self.positions:
            if "_" not in positionI[1]: # checks if it's a Link
                if c.SensorIndexList[currentLink] == 1: #check if it should be a sensor
                    pyrosim.Send_Sensor_Neuron(name = neuronCount, linkName = positionI[1])
                    neuronCount += 1
                currentLink += 1
        for positionI in self.positions:
                if "_" in positionI[1]: # checks if it's a Joint
                    pyrosim.Send_Motor_Neuron(name = neuronCount, jointName = positionI[1])
                    neuronCount += 1
        
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons , weight = self.weights[currentRow][currentColumn])
        
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)

        self.weights[randomRow,randomColumn] = random.random() * 2 - 1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID