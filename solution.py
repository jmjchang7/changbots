import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
import math

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        # initialize variables
        self.startX,self.startY,self.startZ = 0,0,3
        self.dimensionsList = [] #list of lists that holds dimensions for each cube in order. For example, 0 index is [x dim, y dim, z dim]
        self.positionsList = [] #list of ([pos_x, pos_y, pos_z], "Name") that holds positions and name of each cube AND link in order. 
        
        self.armList = [0] * c.numLinks # list of how many arms each snake link has
        for i in range(c.numLinks):
            self.armList[i] = random.randint(0, 2)

        self.armDimsList = [] #list of [x, y, z] dimensions for arms
        self.armPosList = [] #list of ([x_pos, y_pos, z_pos], "Name", sizeX) for arms AND arm joints. sizeX = the max X dimension

        self.legDimsList = [] #list of [x, y, z] dimensions for legs
        self.legPosList = [] #list of ([x_pos, y_pos, z_pos], "Name", spineX, armY) for legs AND leg joints. spineX = the max X dimension, armY = max Y dimension

        def Generate_Link_Dims():
            x = random.random()*0.5 + 0.5
            y = random.random()*0.5 + 0.5
            z = random.random()*0.5 + 0.5

            return [x, y, z]
        
        def Generate_Arm_Dims(sizeX):
            # ARM X Dimension CAN'T be wider than the current snake link's x dim!

            x = (random.random() * 0.5 + 0.5) * sizeX
            y = random.random() * 0.5 + 0.5
            z = random.random() * 0.5 + 0.5

            return [x, y, z, sizeX]
        
        def Generate_Leg_Dims(spineX, armY):
            # LEG Y Dimension CAN'T be wider than the current arm's y dim!

            x = (random.random() * 0.5 + 0.5) * spineX
            y = (random.random() * 0.5 + 0.5) * armY
            z = random.random()* 0.5 + 0.5

            return [x, y, z, spineX, armY]
        
        def Make_First_Single_Arm(armDims, sizeY, sizeZ, y_dir):
            self.armDimsList.append(armDims)

            if y_dir == 0:
                y_factor = 1
            else:
                y_factor = -1
            
            if y_dir == 0: # arm in positive y direction
                self.armPosList.append([[self.startX, self.startY + sizeY/2, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
                self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount), armDims[3]])
                leg_chance = random.randint(0, 1)
                
                if leg_chance == 0:
                    pass
                else:
                    legDims = Generate_Leg_Dims(armDims[0], armDims[1])
                    Make_Leg(legDims, armDims, y_factor)

            else: # arm in negative y direction
                self.armPosList.append([[self.startX, self.startY + sizeY/2, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
                self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount), armDims[3]])
                leg_chance = random.randint(0, 1)
                
                if leg_chance == 0:
                    pass
                else:
                    legDims = Generate_Leg_Dims(armDims[0], armDims[1])
                    Make_Leg(legDims, armDims, y_factor)
            
            self.armCount += 1

        def Make_First_Both_Arms(armDims, sizeY, sizeZ):
            for i in range(2):
                if i == 0:
                    y_factor = 1
                else:
                    y_factor = -1

                self.armDimsList.append(armDims)
                self.armPosList.append([[self.startX, self.startY+sizeY/2*y_factor, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
                self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount), armDims[3]])

                leg_chance = random.randint(0, 1)  
                if leg_chance == 0:
                    pass
                else:
                    legDims = Generate_Leg_Dims(armDims[0], armDims[1])
                    Make_Leg(legDims, armDims, y_factor)

                self.armCount += 1

        def Make_Arm(linkN, sizeX, sizeY):
            if self.armList[linkN] == 0: # no arms
                        pass
            elif self.armList[linkN] == 1: # 1 arm
                armDims = Generate_Arm_Dims(sizeX)

                y_dir = random.randint(0, 1) # decide direction of single arm

                Make_Single_Arm(armDims, sizeX, sizeY, y_dir)

            elif self.armList[linkN] == 2: # 2 arms
                armDims = Generate_Arm_Dims(sizeX)

                Make_Both_Arms(armDims, sizeX, sizeY)

        def Make_Single_Arm(armDims, sizeX, sizeY, y_dir):
            self.armDimsList.append(armDims)

            if y_dir == 0:
                y_factor = 1
            else:
                y_factor = -1
            
            if y_dir == 0: # arm in positive y direction
                self.armPosList.append([[sizeX/2, sizeY/2*y_factor, 0], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
                self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount), armDims[3]])
                leg_chance = random.randint(0, 1)
                
                if leg_chance == 0:
                    pass
                else:
                    legDims = Generate_Leg_Dims(sizeX, armDims[1])
                    Make_Leg(legDims, armDims, y_factor)

            else: # arm in negative y direction
                self.armPosList.append([[sizeX/2, sizeY/2*y_factor, 0], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
                self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount), armDims[3]])
                leg_chance = random.randint(0, 1)
                
                if leg_chance == 0:
                    pass
                else:
                    legDims = Generate_Leg_Dims(sizeX, armDims[1])
                    Make_Leg(legDims, armDims, y_factor)
            
            self.armCount += 1

        def Make_Both_Arms(armDims, sizeX, sizeY):
            for i in range(2):
                if i == 0:
                    y_factor = 1
                else:
                    y_factor = -1

                self.armDimsList.append(armDims)
                self.armPosList.append([[sizeX/2, sizeY/2*y_factor, 0], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
                self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount), armDims[3]])

                leg_chance = random.randint(0, 1)  
                if leg_chance == 0:
                    pass
                else:
                    legDims = Generate_Leg_Dims(sizeX, armDims[1])
                    Make_Leg(legDims, armDims, y_factor)

                self.armCount += 1

        def Make_Leg(legDims, armDims, y_factor):
            self.legDimsList.append(legDims)

            self.legPosList.append([[0, y_factor*(self.armDimsList[self.armCount][1]-legDims[1]/2), -armDims[2]/2], "Arm" + str(self.armCount) + "_Leg" + str(self.legCount)])
            self.legPosList.append([[0, 0, -legDims[2]/2], "Leg" + str(self.legCount), legDims[3], legDims[4]])
            self.legCount += 1

        # CONSTRUCT THE CREATURE

        # make dimensions and positions of each randomized link + its respective joint
        self.linkCount = 0
        self.armCount = 0
        self.legCount = 0
        
        for linkN in range(c.numLinks):
            [sizeX, sizeY, sizeZ] = Generate_Link_Dims()
            self.dimensionsList.append([sizeX, sizeY, sizeZ])

            if linkN == 0: # first link
                self.positionsList.append([[self.startX, self.startY, self.startZ + sizeZ/2], "Link" + str(self.linkCount)]) # first link
                
                self.positionsList.append([[sizeX/2, self.startY, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Link" + str(self.linkCount + 1)]) # first joint
                
                # Not using regular Make_Arm method since first arm joint will have absolute position!
                if self.armList[linkN] == 0: # no arms
                    pass
                elif self.armList[linkN] == 1: # 1 arm
                    armDims = Generate_Arm_Dims(sizeX)

                    y_dir = random.randint(0, 1) # decide direction of single arm

                    Make_First_Single_Arm(armDims, sizeY, sizeZ, y_dir)

                elif self.armList[linkN] == 2: # 2 arms
                    armDims = Generate_Arm_Dims(sizeX)

                    Make_First_Both_Arms(armDims, sizeY, sizeZ)
                
                self.linkCount += 1

            elif linkN < (c.numLinks - 1): # links between first and last link
                
                self.positionsList.append([[sizeX/2, 0, 0], "Link" + str(self.linkCount)]) # makes specified link

                Make_Arm(linkN, sizeX, sizeY) # make arm(s)

                self.positionsList.append([[sizeX, 0, 0], "Link" + str(self.linkCount) + "_Link" + str(self.linkCount + 1)]) #next joint
                self.linkCount += 1

            elif linkN == (c.numLinks - 1): # last link
                self.positionsList.append([[sizeX/2, 0, 0], "Link" + str(self.linkCount)]) #last link (has no next joint)

                Make_Arm(linkN, sizeX, sizeY) # make arm(s)
            
            # TEST - RANDOMIZE EVERYTHING IN CONSTRUCTOR
            # now actually make the "Cubes" and "Joints"
            # SENSOR LISTS FOR ARMS
            self.armSensorList = []
            for i in range(len(self.armDimsList)):
                self.armSensorList.append(random.randint(0, 1))

            self.legSensorList = []
            for i in range(len(self.legDimsList)):
                self.legSensorList.append(random.randint(0, 1))


            self.allPosList = self.positionsList + self.armPosList + self.legPosList
            self.allSensorList = c.SensorIndexList + self.armSensorList + self.legSensorList

            # send sensor and motor neurons
            self.numJoints = 0
            neuronCount = 0
            currentLink = 0
            for positionI in self.allPosList:
                    if "_" not in positionI[1]: # checks if it's a Link
                        if self.allSensorList[currentLink] == 1: #check if it should be a sensor
                            # pyrosim.Send_Sensor_Neuron(name = neuronCount, linkName = positionI[1])
                            neuronCount += 1
                        currentLink += 1
            for positionI in self.allPosList:
                    if "_" in positionI[1]: # checks if it's a Joint
                        # pyrosim.Send_Motor_Neuron( name = neuronCount, jointName = positionI[1])
                        self.numJoints += 1
                        neuronCount += 1
            
            numSensors = self.allSensorList.count(1)
            numMotors = self.numJoints
            self.weights = [[random.random() * 2 - 1 for _ in range(numMotors)] for _ in range(numSensors)]

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Send_Body()
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
        pass

    def Send_Body(self):
        # now actually make the "Cubes" and "Joints"
        # SENSOR LISTS FOR ARMS
        # self.armSensorList = []
        # for i in range(len(self.armDimsList)):
        #     self.armSensorList.append(random.randint(0, 1))

        # self.legSensorList = []
        # for i in range(len(self.legDimsList)):
        #     self.legSensorList.append(random.randint(0, 1))   

        for linkN in range(c.numLinks-1):
            pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
            currentLink = 0
            for positionI in self.positionsList: # EACH JOINT IN SPINE
                if "_" not in positionI[1]: # if not Joint
                    if c.SensorIndexList[currentLink] == 1: # if sensor, set green
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.dimensionsList[currentLink], color_string = '    <color rgba= "0 255.0 0.0 1.0"/>', color = 'Green')
                    else:
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.dimensionsList[currentLink])
                    currentLink += 1
                else: # if Joint
                    pyrosim.Send_Joint(name = positionI[1] , parent= positionI[1].split('_')[0] , child = positionI[1].split('_')[1] , type = "revolute", position = positionI[0], jointAxis = "0 0 1")
            self.linkCount = 0

            currentArm = 0
            for positionI in self.armPosList: # EACH ARM 
                if "_" not in positionI[1]: # if not Joint
                    if self.armSensorList[currentArm] == 1: # if sensor, set green
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.armDimsList[currentArm], color_string = '    <color rgba= "0 255.0 0.0 1.0"/>', color = 'Green')
                    else:
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.armDimsList[currentArm])
                    currentArm += 1
                else: # if Joint
                    pyrosim.Send_Joint(name = positionI[1] , parent= positionI[1].split('_')[0] , child = positionI[1].split('_')[1] , type = "revolute", position = positionI[0], jointAxis = "0 1 0")
            # self.armCount = 0

            currentLeg = 0
            for positionI in self.legPosList: # EACH ARM 
                if "_" not in positionI[1]: # if not Joint
                    if self.legSensorList[currentLeg] == 1: # if sensor, set green
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.legDimsList[currentLeg], color_string = '    <color rgba= "0 255.0 0.0 1.0"/>', color = 'Green')
                    else:
                        pyrosim.Send_Cube(name = positionI[1], pos=positionI[0], size=self.legDimsList[currentLeg])
                    currentLeg += 1
                else: # if Joint
                    pyrosim.Send_Joint(name = positionI[1] , parent= positionI[1].split('_')[0] , child = positionI[1].split('_')[1] , type = "revolute", position = positionI[0], jointAxis = "0 1 0")
            # self.legCount = 0

        pyrosim.End()

    def Send_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # self.allPosList = self.positionsList + self.armPosList + self.legPosList
        # self.allSensorList = c.SensorIndexList + self.armSensorList + self.legSensorList
        self.numJoints = 0 # for counting all joints (to make motors later)

        # send sensor and motor neurons
        neuronCount = 0
        currentLink = 0
        for positionI in self.allPosList:
                if "_" not in positionI[1]: # checks if it's a Link
                    if self.allSensorList[currentLink] == 1: #check if it should be a sensor
                        pyrosim.Send_Sensor_Neuron(name = neuronCount, linkName = positionI[1])
                        neuronCount += 1
                    currentLink += 1
        for positionI in self.allPosList:
                if "_" in positionI[1]: # checks if it's a Joint
                    pyrosim.Send_Motor_Neuron( name = neuronCount, jointName = positionI[1])
                    self.numJoints += 1
                    neuronCount += 1
        
        numSensors = self.allSensorList.count(1)
        numMotors = self.numJoints
        
        for currentRow in range(numSensors):
            for currentColumn in range(numMotors):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + numSensors , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):

        def Mutate_Synapses():
            # Randomize synapse connections
            randomRow = random.randint(0, c.numSensorNeurons-1)
            randomColumn = random.randint(0, c.numMotorNeurons-1)

            self.weights[randomRow][randomColumn] = random.random() * 2 - 1

        def Mutate_Arm():
            # Need to change: dimensions + positions of mutated arms, and positions of any joints connecting that arm to its spinal unit

            # First, obtain indices of position list that hold the arm links
            changeArmInds = [] # holds list of [index in the dimension list, index in the position list] of the arms to be changed
            for i in range(len(self.allPosList)):
                if "_" not in self.allPosList[i][1] and "Arm" in self.allPosList[i][1]:
                    pos_ind = i
                    temp_arm_ind = self.allPosList[i][1].find("Arm")
                    dim_ind = int(self.allPosList[i][1][(temp_arm_ind+3):]) # find the X in "ArmX" of the name to find the index in the dimension list
                    changeArmInds.append([dim_ind, pos_ind])

            # Randomize number of: arms in which to change sizes
            numChangeArms = random.randint(0, self.armCount)
            if numChangeArms == 0:
                return
            # Change arms one by one until the number of arms to change (numChangeArms) becomes 0
            while numChangeArms > 0 and changeArmInds:
                # shuffle order of arm randomization, then choose arm
                random.shuffle(changeArmInds)
                armInd = changeArmInds.pop()
                # make new random arm dimensions, replace old ones
                oldArmDims = self.armDimsList[armInd[0]]
                changeX = oldArmDims[0] * (random.random() + 0.5)
                if changeX > self.allPosList[armInd[1]][2]:
                    changeX = 0.9 * self.allPosList[armInd[1]][2]
                changeY = oldArmDims[1] * (random.random() + 0.5)
                changeZ = oldArmDims[2] * (random.random() + 0.5)
                newArmDims = [changeX, changeY, changeZ]
                self.armDimsList[armInd[0]] = newArmDims
                # replace old arm link position with new one
                y_factor = math.copysign(1, self.allPosList[armInd[1]][0][1])
                newYPos = newArmDims[1]/2 * y_factor
                newArmPos = [0, newYPos, 0]
                self.allPosList[armInd[1]][0] = newArmPos
                # replace old arm-leg joint position with new one
                changeJointInds = []
                for i in range(len(self.allPosList)):
                    if "Arm" + str(armInd[0]) + "_Leg" in self.allPosList[i][1]:
                        changeJointInds.append(i)
                        leg_ind = self.allPosList[i][1].find("Leg") 
                        leg_num = int(self.allPosList[i][1][(leg_ind+3):]) # get the leg number
                if len(changeJointInds) > 0:
                    old_leg_y = self.legDimsList[leg_num][1]
                    old_joint_pos_y = self.allPosList[changeJointInds[0]][0][1]
                    y_factor = old_joint_pos_y/(oldArmDims[1]-old_leg_y/2)
                    changeY = y_factor * (newArmDims[1] - old_leg_y/2) # new joint y: y_factor * (newArmY - oldLegY/2)
                    changeZ = -newArmDims[2]/2 # new joint z: -newLegZ/2
                    self.allPosList[changeJointInds[0]][0] = [0, changeY, changeZ]

                # Change the ymax of the leg associated with the changed arm
                # First, extract the leg connected to the changed arm
                leg_changedYMax = ""
                for positionI in self.allPosList:
                    if "_" in positionI[1] and ("Arm " + str(armInd[0])) in positionI[1]: #find leg through connected joint
                        leg_index = positionI[1].find("Leg")
                        leg_changedYMax = positionI[1][leg_index:] # "LegX"

                # change the ymax of the leg
                for i in range(len(self.allPosList)):
                    if self.allPosList[i][1] == leg_changedYMax:
                        self.allPosList[i][3] = changeY
                
                numChangeArms -= 1

        def Mutate_Leg():
            # First, obtain indices of position list that hold the leg links
            changeLegInds = [] # holds list of [index in the dimension list, index in the position list] of the legs to be changed
            for i in range(len(self.allPosList)):
                if "_" not in self.allPosList[i][1] and "Leg" in self.allPosList[i][1]:
                    pos_ind = i
                    temp_leg_ind = self.allPosList[i][1].find("Leg")
                    dim_ind = int(self.allPosList[i][1][(temp_leg_ind+3):]) # find the X in "ArmX" of the name to find the index in the dimension list
                    changeLegInds.append([dim_ind, pos_ind])

            # Randomize number of: arms in which to change sizes
            numChangeLegs = random.randint(0, self.legCount)
            if numChangeLegs == 0:
                return
            # Change leg one by one until the number of leg to change (numChangeLegs) becomes 0
            while numChangeLegs > 0 and changeLegInds:
                # shuffle order of leg randomization, then choose leg
                random.shuffle(changeLegInds)
                legInd = changeLegInds.pop()
                # make new random leg dimensions, replace old ones
                oldLegDims = self.legDimsList[legInd[0]]
                changeX = oldLegDims[0] * (random.random() + 0.5)
                if changeX > self.allPosList[legInd[1]][2]:
                    changeX = 0.9 * self.allPosList[legInd[1]][2]
                changeY = oldLegDims[1] * (random.random() + 0.5)
                if changeY > self.allPosList[legInd[1]][3]:
                    changeY = 0.9 * self.allPosList[legInd[1]][3]
                changeZ = oldLegDims[2] * (random.random() + 0.5)
                newLegDims = [changeX, changeY, changeZ]
                self.legDimsList[legInd[0]] = newLegDims

                # replace old arm link position with new one
                newZPos = -newLegDims[2]/2
                newLegPos = [0, 0, newZPos]
                self.allPosList[legInd[1]][0] = newLegPos

                # replace old arm-leg joint position with new one
                changeJointInds = []
                for i in range(len(self.allPosList)):
                    if "_Leg" + str(legInd[0]) in self.allPosList[i][1]:
                        changeJointInds.append(i)
                        armInd = int(self.allPosList[i][1].split("_")[0][3:]) # get the arm index out - we need to acess the armY dim when replacing the joint position
                if len(changeJointInds) > 0:
                    old_arm_y = self.armDimsList[armInd][1]
                    old_arm_z = self.armDimsList[armInd][2]
                    old_joint_pos_y = self.allPosList[changeJointInds[0]][0][1]
                    y_factor = old_joint_pos_y/(old_arm_y - oldLegDims[1]/2)
                    changeY = y_factor * (old_arm_y - newLegDims[1]/2) # new joint y: y_factor * (oldArmY - newLegY/2)
                    self.allPosList[changeJointInds[0]][0] = [0, changeY, old_arm_z]

            numChangeLegs -= 1

        # Change synapse connections
        Mutate_Synapses()
        # Change arm size
        Mutate_Arm()
        #Change leg size
        Mutate_Leg()

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID