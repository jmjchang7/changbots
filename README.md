# changbots

### Table of Contents  
* [Intro](#intro)
* [Body Generation](#body-generation)
    - [Spine](#spine)
    - [Arms](#arms)
* [Brain Generation](#brain-generation)
* [Morphospace](#morphospace)
* [Evolution](#evolution)
* [The Parallel Hill Climber](#the-parallel-hill-climber)
* [Results](#results)
* [References](#references)


## Intro
Insert video link here: 

Insert gif here:


## Body Generation:
The body is generated by a random stepwise process consisting of spine, arm, and leg generation, respectively.
![IMG_39B3E5731AD0-1](https://user-images.githubusercontent.com/120343561/220268784-290b3f50-5b5e-4d8d-92db-d82f0f293525.jpeg)
Figure 1: Robot Phenotype

Source: Adapted from _Figure 3: Designed examples of genotype graphs and corresponding creature morphologies_ from [1]


### Spine:
A similar process to the snake body generation was kept: for a randomly generated total number of links (**numLinks**), a random snake in the x-direction was generated:
1. First link and joints are made (since they are both made using absolute positions)
2. For every other link before the last: a joint + link pair is made (using relative positions)
3. The last link is made.      
This creates the spine of the snake, which can be seen extending in the x-axis of the figure above.

### Arms:
For each cube in the "snake spine," a random number was generated (0, 1, or 2) for the number of arms attached to the spinal unit. Different cases are listed below:
1. If 0 arms, a "pass" was implemented.
2. If 1 arm, another variable, **y_dir** (random int 0 or 1) was used to make the randomized arm in the +y or -y direction of the spinal unit, as well as the joint connecting the new arm to its spinal unit.
4. If 2 arms, randomized arms were made in both the +y and -y directions of the spinal unit, as well as their respective joints.  
As can be seen on Figure 1, the formation of 2 arms on a spinal unit showed pseudo-evolution to a **lizard-like creature**.
_Note:_ An arm can't be wider in the x-direction than its spinal unit. Otherwise, it would overlap with it.

### Legs:
For each arm, a variable called **leg_chance** (random int 0 or 1) randomly decided whether or not the arm would have an attached arm.
1. If 0 legs, a "pass" was implemented.
2. If 1 leg, a randomized leg was added to the bottom (-z direction) of the arm, as well as its respective arm-leg joint.
As can be seen on Figure 1, the formation of legs on each arm of a spinal unit showed pseudo-evolution to a **horse-like creature**.
_Note:_ A leg can't be wider in the y-direction than its arm, and it can't be wider in the x-direction than the spinal unit that arm is connected to. Otherwise, it would overlap with either of the two.
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

## Results:

Insert graphs here

## References:
Sims, Karl. “Evolving 3D Morphology and Behavior by Competition.” Artificial Life, vol. 1, no. 4, 1994, pp. 353–372., https://doi.org/10.1162/artl.1994.1.4.353. 



