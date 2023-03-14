# changbots: evolutionary robots

### Table of Contents  
* [Intro](#intro)
* [Body Generation](#body-generation)
    - [Spine](#spine)
    - [Arms](#arms)
    - [Legs](#legs)
* [Brain Generation](#brain-generation)
* [Morphospace](#morphospace)
* [Evolution](#evolution)
* [The Parallel Hill Climber](#the-parallel-hill-climber)
* [Results](#results-(plots))
    - [Plots](#plots)
    - [gifs](#gifs)
* [References](#references)
* [How to Run Changbots](#how-to-run-changbots)


## Intro
Welcome to Changbots!

Here's a little teaser of what's contained in this project:
  
![ludo final project gif](https://user-images.githubusercontent.com/120343561/224871717-ec6c993c-60b8-4877-a6d7-c3b8431bf372.gif)

And here's a video summary, if you don't wanna read the details of the rest of this README 😩 

<a href="https://www.youtube.com/watch?v=gMaUwJvYOIA">
  <img src="https://img.youtube.com/vi/gMaUwJvYOIA/maxresdefault.jpg" alt="VIDEO_TITLE">
</a>  

[changbot video presentation](https://youtu.be/gMaUwJvYOIA)

This project could not have been done without:
1. r/ludobots, https://www.reddit.com/r/ludobots/, and
2. pyrosim, https://www.thunderheadeng.com/pyrosim

The methods of robot building and evolving are built on methods used in the first source, and the second source allowed for the use of a 3D-graphical interface with which to present the visual results.


## Body Generation:
The body is generated by a random stepwise process consisting of spine, arm, and leg generation, respectively. Each block is called a **link**, and each block is connected by a **joint**, which isn't visible.
![IMG_39B3E5731AD0-1](https://user-images.githubusercontent.com/120343561/220268784-290b3f50-5b5e-4d8d-92db-d82f0f293525.jpeg)
Figure 1: Robot Phenotype

Source: Adapted from _Figure 3: Designed examples of genotype graphs and corresponding creature morphologies_ from [1]


### Spine:
A similar process to the snake body generation was kept: for a randomly generated total number of links (**numLinks**), a random snake in the x-direction was generated:
1. First link and joints are made (since they are both made using absolute positions)
2. For every other link before the last: a joint + link pair is made (using relative positions)
3. The last link is made.      
This creates the spine of the snake, which can be seen extending in the x-axis of the figure above. The spinal unit joints allow for wiggling in the xy-plane.

### Arms:
For each cube in the "snake spine," a random number was generated (0, 1, or 2) for the number of arms attached to the spinal unit. Different cases are listed below:
1. If 0 arms, a "pass" was implemented.
2. If 1 arm, another variable, **y_dir** (random int 0 or 1) was used to make the randomized arm in the +y or -y direction of the spinal unit, as well as the joint connecting the new arm to its spinal unit.
4. If 2 arms, randomized arms were made in both the +y and -y directions of the spinal unit, as well as their respective joints.  
As can be seen on Figure 1, the formation of 2 arms on a spinal unit showed pseudo-evolution to a **lizard-like creature**. The arm-spine joints rotate in the xz-plane.  
_Note:_ An arm can't be wider in the x-direction than its spinal unit. Otherwise, it would overlap with it.

### Legs:
For each arm, a variable called **leg_chance** (random int 0 or 1) randomly decided whether or not the arm would have an attached arm.
1. If 0 legs, a "pass" was implemented.
2. If 1 leg, a randomized leg was added to the bottom (-z direction) of the arm, as well as its respective arm-leg joint.
As can be seen on Figure 1, the formation of legs on each arm of a spinal unit showed pseudo-evolution to a **horse-like creature**.   
_Note:_ A leg can't be wider in the y-direction than its arm, and it can't be wider in the x-direction than the spinal unit that arm is connected to.    Otherwise, it would overlap with either of the two. The arm-leg joints also rotate in the xz-plane.  
### Brain Generation:
![IMG_2B480D5020CD-1](https://user-images.githubusercontent.com/120343561/220411380-6b2ea42c-117f-4dc5-a5ff-a5745487aae9.jpeg)
Figure 2: Robot Genetic Storage and Brain Synapse Construction

Source: Adapted from _Figure 6b: The phenotype "brain"..._ from [1]
  
The brain is made of a network of synapses, connecting sensor and motor neurons of the creature.
1. A random subset of all links (spinal units, arms, and legs) is chosen to be sensor neurons.
2. ALL joints are motor neurons.
3. The sensor identity is stored in respective lists for each category (spinal unit, arm, or leg). After constructing the whole creature, this list is iterated through in order to make the brain network, as shown in the diagram above.

Since the sensor neurons are placed randomly, the brain's intelligence could vary greatly: a brain could be built on sensors on the spine, arms, or legs. A sensor on a leg could affect a motor on the same leg, or a leg on a completely different spinal unit.

## Morphospace:
Possible body shapes and movements:
1. **Snake**: if no arms (and thus legs) are generated, the creature will resemble the same creature as created in Assignment 6.
2. **Lizard**: if arms are generated on both sides of a spinal unit (without legs), the creature will resemble a 2-D lizard.
3. **Horse**: if legs are generated (on both sides) on an arm, the creature will resemble a 3-D horse.

The snake will slither in the XY plane.
The lizard will do the same.
The horse, though, will use its legs to walk forward.

## Evolution:
Evolution occurs via a series of random mutations.  
![IMG_F43951E6EDD1-1](https://user-images.githubusercontent.com/120343561/224627996-06f83c8a-b5db-460b-8fc3-82f1ca33bf22.jpeg)
Figure 3: Robot Mutation


Mutations occur during each generation, from the parent to the child. In this section, the evolution from one parent to its child will be outlined. In the next section, the bigger-picture process of evolution across time in the entire population will be described (aka the Parallel Hill Climber).

Mutations can occur in two ways:
1. Body mutation: random arms and legs of the robot are resized randomly.
2. Brain mutation: the sensor-motor connections, called _synapses_, are weighted differently, randomly. This means that some motors will have a weaker or stronger connection to their sensors, leading to more or less movement in some area of the robot.  

Collectively, this will change the locomotive ability of the robot, which is measured by the **fitness function**.
For changbots, this fitness function is defined as the distance the robot travels away from the origin. The greater the distance, the greater the fitness value of the robot.

Evolution occurs when **the fitness of the child is greater than that of the parent.** If this is the case, the child robot design will survive over its parent to continue as the next generation. If not, the parent robot design will stay unchanged for the next generation.



## The Parallel Hill Climber
![IMG_C5E75C24F3BB-1](https://user-images.githubusercontent.com/120343561/224628231-ac589ffc-468e-4377-988e-dc0868a6715b.jpeg)   
Figure 4: Parallel Hill Climber mechanism


The parallel hill climber model is the means by which changbots evolve.
1. An initial population is created. Say 5 random robots. We call these the first **parents**, Generation 1.
2. These robots are duplicated, then mutated to create the first **children**, Generation 2.
3. Across the population, children will replace their parents if they have better fitness. If not, the parent will prevail to continue the generation.
4. This process repeats for however many generations exist.
5. At the end of the process, each robot in its population represents the most fit of its "species," or column. 
6. The most fit robot of all is selected as the **best robot**. 
7. This whole process can be repeated! Each run of the parallel hill climber is called a **seed**. So if there were 5 seeds, imagine 5 of these diagrams running each after the other.

## Results:
The simulation was run for 5 seeds on two occasions, totaling to 10 seeds. Each run contained a population size of 10, and lasted for 50 generations.
The total amount of times run thus amounted to: 10 pop x 100 gen x 10 seeds = 10,000 simulations.  

Each 10 pop x 10 gen run took about 2 minutes, so the total time was around 200 minutes, or 3 hours and 20 minutes.
50,000 simulations would have taken around 16 hours and 40 minutes. This was not realistic for me to run, as I had to use my computer to study for other finals before the project deadline 😭. However, a good representation of the evolution process was still shown.   
   
      
### Plots:   
<img width="971" alt="evolcurves" src="https://user-images.githubusercontent.com/120343561/224925681-f5b147f1-8c05-4acb-96b7-58d30f8c6f29.png"> 
   
Figure 5: Evolution curves, Seeds 1-5 (plot 1), Seeds 6-10 (plot 2)   

In the evolution time span of the results, it could be seen that the fitness was around 20. This resulted in pretty good locomotive behavior, as can be seen in the gifs below. Interestingly, all of the creatures after this amount of evolution seemed to be pretty big. They all had around 4-5 spinal units, rather than 2-3. While big creatures are cool, when I ran changbots with a smaller evolution span (around 10-50 generations), there was a more visually appealing, simple locomotion that seemed to die out. One reason this might've occurred is due to the bigger size of the creatures with more spinal units. Since they're bigger, they could be sensed further out from the origin, signalling a greater fitness, even if they didn't move as much as the smaller creatures did. Despite this, there was a lot of diverse behavior in the changbots! See below.
   
   
### gifs:
   
Creatures 1, 2, 3, 5 (4 is shown in intro gif):   
![final evolved 1](https://user-images.githubusercontent.com/120343561/224875776-d426d873-5e27-465a-b17f-a9f8cf8a1ae9.gif) ![final evolved 2](https://user-images.githubusercontent.com/120343561/224875844-b9c88d68-314d-4b2e-a500-8a0ced536949.gif) ![final evolved 3](https://user-images.githubusercontent.com/120343561/224876984-0cdaf865-b881-4605-868e-13e1b7689286.gif) ![final evolved 5](https://user-images.githubusercontent.com/120343561/224877804-7794d6a7-b4a4-4005-b661-871ed6146fb7.gif)



Creatures 6, 10 (7-9 showed similar behavior):   
![final evolved 6](https://user-images.githubusercontent.com/120343561/224880120-1218c065-3b7e-4126-b524-4604b5824beb.gif) ![final evolved 10](https://user-images.githubusercontent.com/120343561/224926418-35e753d4-54fd-4b84-9957-6970f44cd52b.gif)

## How to Run Changbots:
In order to run changbots, first:
1. Download this repository.
2. Then, run the "button.py" file.
3. If you want to play with any of the parameters of the evolution (such as number of generations, population size, number of seeds, etc.), find the "constants.py" folder.
4. Enjoy!


## References:
Sims, Karl. “Evolving 3D Morphology and Behavior by Competition.” Artificial Life, vol. 1, no. 4, 1994, pp. 353–372., https://doi.org/10.1162/artl.1994.1.4.353. 



