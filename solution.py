import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.weights = [[random.random() * 2 - 1 for _ in range(c.numMotorNeurons)] for _ in range(c.numSensorNeurons)]
        self.myID = nextAvailableID

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Send_Body()
        self.Send_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.001)
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
        self.startX,self.startY,self.startZ = 0,0,3
        self.dimensionsList = [] #list of lists that holds dimensions for each cube in order. For example, 0 index is [x dim, y dim, z dim]
        self.positionsList = [] #list of ([position list], "Name") that holds positions and name of each cube AND link in order. 
        
        self.armList = [0] * c.numLinks # list of how many arms each snake link has
        for i in range(c.numLinks):
            self.armList[i] = random.randint(0, 2)

        self.armDimsList = [] #list of [x, y, z] dimensions for arms
        self.armPosList = [] #list of ([x_pos, y_pos, z_pos], "Name") for arms AND arm joints

        self.legDimsList = [] #list of [x, y, z] dimensions for legs
        self.legPosList = [] #list of ([x_pos, y_pos, z_pos], "Name") for legs AND leg joints
          
        # make dimensions and positions of each randomized link + its respective joint
        self.linkCount = 0
        self.armCount = 0
        self.legCount = 0
        for linkN in range(c.numLinks):
            [sizeX, sizeY, sizeZ] = self.Generate_Link_Dims()
            if linkN == 0:
                sizeX += c.mutator
            self.dimensionsList.append([sizeX, sizeY, sizeZ])

            if linkN == 0: # first link
                self.positionsList.append([[self.startX, self.startY, self.startZ + sizeZ/2], "Link" + str(self.linkCount)]) # first link
                
                self.positionsList.append([[sizeX/2, self.startY, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Link" + str(self.linkCount + 1)]) # first joint
                
                # Not using regular Make_Arm method since first arm joint will have absolute position!
                if self.armList[linkN] == 0: # no arms
                    pass
                elif self.armList[linkN] == 1: # 1 arm
                    armDims = self.Generate_Arm_Dims(sizeX)

                    y_dir = random.randint(0, 1) # decide direction of single arm

                    self.Make_First_Single_Arm(armDims, sizeY, sizeZ, y_dir)

                elif self.armList[linkN] == 2: # 2 arms
                    armDims = self.Generate_Arm_Dims(sizeX)

                    self.Make_First_Both_Arms(armDims, sizeY, sizeZ)
                
                self.linkCount += 1

            elif linkN < (c.numLinks - 1): # links between first and last link
                
                self.positionsList.append([[sizeX/2, 0, 0], "Link" + str(self.linkCount)]) # makes specified link

                self.Make_Arm(linkN, sizeX, sizeY) # make arm(s)

                self.positionsList.append([[sizeX, 0, 0], "Link" + str(self.linkCount) + "_Link" + str(self.linkCount + 1)]) #next joint
                self.linkCount += 1

            elif linkN == (c.numLinks - 1): # last link
                self.positionsList.append([[sizeX/2, 0, 0], "Link" + str(self.linkCount)]) #last link (has no next joint)

                self.Make_Arm(linkN, sizeX, sizeY) # make arm(s)

    def Send_Body(self):
        # now actually make the "Cubes" and "Joints"
        # SENSOR LISTS FOR ARMS
        self.armSensorList = []
        for i in range(len(self.armDimsList)):
            self.armSensorList.append(random.randint(0, 1))

        self.legSensorList = []
        for i in range(len(self.legDimsList)):
            self.legSensorList.append(random.randint(0, 1))   

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
            self.armCount = 0

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
            self.legCount = 0

        pyrosim.End()

    def Send_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        self.allPosList = self.positionsList + self.armPosList + self.legPosList
        self.allSensorList = c.SensorIndexList + self.armSensorList + self.legSensorList

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
                    neuronCount += 1
        
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn + c.numSensorNeurons , weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)

        self.weights[randomRow][randomColumn] = random.random() * 2 - 1

        c.mutator *= random.random() + 0.1

    def Set_ID(self, nextAvailableID):
        self.myID = nextAvailableID

    def Generate_Link_Dims(self):
        x = random.random()*0.5 + 0.5
        y = random.random()*0.5 + 0.5
        z = random.random()*0.5 + 0.5

        return [x, y, z]

    def Generate_Arm_Dims(self, sizeX):
        # ARM X Dimension CAN'T be wider than the current snake link's x dim!

        x = (random.random() * 0.5 + 0.5) * sizeX
        y = random.random() * 0.5 + 0.5
        z = random.random() * 0.5 + 0.5

        return [x, y, z]

    def Generate_Leg_Dims(self, spineX, armY):
        # LEG Y Dimension CAN'T be wider than the current arm's y dim!

        x = (random.random() * 0.5 + 0.5) * spineX
        y = (random.random() * 0.5 + 0.5) * armY
        z = random.random()* 0.5 + 0.5

        return [x, y, z]
    
    def Make_First_Single_Arm(self, armDims, sizeY, sizeZ, y_dir):
        self.armDimsList.append(armDims)

        if y_dir == 0:
            y_factor = 1
        else:
            y_factor = -1
        
        if y_dir == 0: # arm in positive y direction
            self.armPosList.append([[self.startX, self.startY + sizeY/2, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
            self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount)])
            leg_chance = random.randint(0, 1)
            
            if leg_chance == 0:
                pass
            else:
                legDims = self.Generate_Leg_Dims(armDims[0], armDims[1])
                self.Make_Leg(legDims, armDims, y_factor)

        else: # arm in negative y direction
            self.armPosList.append([[self.startX, self.startY + sizeY/2, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
            self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount)])
            leg_chance = random.randint(0, 1)
            
            if leg_chance == 0:
                pass
            else:
                legDims = self.Generate_Leg_Dims(armDims[0], armDims[1])
                self.Make_Leg(legDims, armDims, y_factor)
        
        self.armCount += 1

    def Make_First_Both_Arms(self, armDims, sizeY, sizeZ):
        for i in range(2):
            if i == 0:
                y_factor = 1
            else:
                y_factor = -1

            self.armDimsList.append(armDims)
            self.armPosList.append([[self.startX, self.startY+sizeY/2*y_factor, self.startZ + sizeZ/2], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
            self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount)])

            leg_chance = random.randint(0, 1)  
            if leg_chance == 0:
                pass
            else:
                legDims = self.Generate_Leg_Dims(armDims[0], armDims[1])
                self.Make_Leg(legDims, armDims, y_factor)

            self.armCount += 1
    
    def Make_Arm(self, linkN, sizeX, sizeY):
        if self.armList[linkN] == 0: # no arms
                    pass
        elif self.armList[linkN] == 1: # 1 arm
            armDims = self.Generate_Arm_Dims(sizeX)

            y_dir = random.randint(0, 1) # decide direction of single arm

            self.Make_Single_Arm(armDims, sizeX, sizeY, y_dir)

        elif self.armList[linkN] == 2: # 2 arms
            armDims = self.Generate_Arm_Dims(sizeX)

            self.Make_Both_Arms(armDims, sizeX, sizeY)

    def Make_Single_Arm(self, armDims, sizeX, sizeY, y_dir):
        self.armDimsList.append(armDims)

        if y_dir == 0:
            y_factor = 1
        else:
            y_factor = -1
        
        if y_dir == 0: # arm in positive y direction
            self.armPosList.append([[sizeX/2, sizeY/2*y_factor, 0], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
            self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount)])
            leg_chance = random.randint(0, 1)
            
            if leg_chance == 0:
                pass
            else:
                legDims = self.Generate_Leg_Dims(sizeX, armDims[1])
                self.Make_Leg(legDims, armDims, y_factor)

        else: # arm in negative y direction
            self.armPosList.append([[sizeX/2, sizeY/2*y_factor, 0], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
            self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount)])
            leg_chance = random.randint(0, 1)
            
            if leg_chance == 0:
                pass
            else:
                legDims = self.Generate_Leg_Dims(sizeX, armDims[1])
                self.Make_Leg(legDims, armDims, y_factor)
        
        self.armCount += 1

    def Make_Both_Arms(self, armDims, sizeX, sizeY):
        for i in range(2):
            if i == 0:
                y_factor = 1
            else:
                y_factor = -1

            self.armDimsList.append(armDims)
            self.armPosList.append([[sizeX/2, sizeY/2*y_factor, 0], "Link" + str(self.linkCount) + "_Arm" + str(self.armCount)])
            self.armPosList.append([[0, armDims[1]/2*y_factor, 0], "Arm" + str(self.armCount)])

            leg_chance = random.randint(0, 1)  
            if leg_chance == 0:
                pass
            else:
                legDims = self.Generate_Leg_Dims(sizeX, armDims[1])
                self.Make_Leg(legDims, armDims, y_factor)

            self.armCount += 1

    def Make_Leg(self, legDims, armDims, y_factor):
        self.legDimsList.append(legDims)

        self.legPosList.append([[0, y_factor*(self.armDimsList[self.armCount][1]-legDims[1]/2), -armDims[2]/2], "Arm" + str(self.armCount) + "_Leg" + str(self.legCount)])
        self.legPosList.append([[0, 0, -legDims[2]/2], "Leg" + str(self.legCount)])
        self.legCount += 1