import pyrosim.pyrosim as pyrosim

length,width,height = 1,1,1
x,y,z=0,0,0.5

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name="Box", pos=[x-2,y-2,z], size=[length,width,height])
    pyrosim.End()


def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0,0,0.5], size=[length,width,height])
    pyrosim.Send_Joint(name = "Torso_Body" , parent= "Torso" , child = "Body" , type = "revolute", position = [0.5,0,1])
    pyrosim.Send_Cube(name="Body", pos=[0.5,0,0.5], size=[length,width,height])
    pyrosim.Send_Joint(name = "Body_Leg" , parent= "Body" , child = "Leg" , type = "revolute", position = [1,0,0])
    pyrosim.Send_Cube(name="Leg", pos=[0.5,0,-0.5], size=[length,width,height])
    pyrosim.End()

Create_World()
Create_Robot()