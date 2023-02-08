# changbots

Project Runway:

1. Runway creation: In order to create the runway, I took the initial block from the world.sdf file and extended its x dimension and raised the z dimension to resemble an elevated runway. It was important to note that the runway extended in the x dimension such that the robot would walk in the -x direction, as already defined by its fitness function.

2. Robot generation: To match this change in the runway, I changed the positions of all the limbs and joints in the robot defined by absolute positions. I also added an extra back leg to the robot (in the direction of movement). To do this, I simply added the height of the runway to all the absolute z dimensions of the robot.

3. The fitness function: This function essentially measures how well the robot moves in the -x-direction in a given amount of time. The function is calculated by obtaining the x position of the robot's base position, a variable that is determined by the robot's overall position on the coordinates of the world.
