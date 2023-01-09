import pyrosim.pyrosim as pyrosim
pyrosim.Start_SDF("boxes.sdf")
length,width,height = 1,1,1

for x in range(5):
    for y in range(5):
        for z in range (10):
            pyrosim.Send_Cube(name="Box", pos=[x,y,z], size=[length*0.9**z,width*0.9**z,height*0.9**z])

pyrosim.End()