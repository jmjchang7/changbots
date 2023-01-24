
from world import WORLD
from robot import ROBOT

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)

        self.world = WORLD()
        self.robot = ROBOT()

        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()

    def Run(self):
        for t in range(1000):
            time.sleep(1/60)
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)

    def __del__(self):
        p.disconnect()