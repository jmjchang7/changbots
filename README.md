# changbots

##### Table of Contents  
[Intro](#intro)  
[Body Generation](#body-generation)  
[Brain Generation](#brain-generation) 


## Intro
Insert video link here: 

Insert gif here:


## Body Generation: <a name="body-generation"></a>
![IMG_39B3E5731AD0-1](https://user-images.githubusercontent.com/120343561/220268784-290b3f50-5b5e-4d8d-92db-d82f0f293525.jpeg)

Figure 1: Robot Phenotype

Source: Adapted from _Figure 3: Designed examples of genotype graphs and corresponding creature morphologies_ from [1]


### Spine: <a name="spine"></a>
A similar process to the snake body generation was kept: for a randomly generated total number of links (**numLinks**), a random snake in the x-direction was generated:
1. First link and joints are made (since they are both made using absolute positions
2. For every other link before the last: joint + link is made (using relative positions)
3. Last link is made

### Arms: <a name="arms"></a>
For each cube in the "snake spine," a random number was generated (0, 1, or 2) for the number of arms attached to the spinal unit. Different cases are listed below:
1. If 0 arms, a "pass" was implemented.
2. If 1 arm, another variable, **y_dir** (random int 0 or 1) was used to make the randomized arm in the +y or -y direction of the spinal unit, as well as the joint connecting the new arm to its spinal unit.
4. If 2 arms, randomized arms were made in both the +y and -y directions of the spinal unit, as well as their respective joints.
As can be seen on the diagram, the formation of 2 arms on a spinal unit showed pseudo-evolution to a **lizard-like creature**.

### Legs:
For each arm, a variable called **leg_chance** (random int 0 or 1) randomly decided whether or not the arm would have an attached arm.
1. If 0 legs, a "pass" was implemented.
2. If 1 leg, a randomized leg was added to the bottom (-z direction) of the arm, as well as its respective arm-leg joint.
As can be seen on the diagram, the formation of legs on each arm of a spinal unit showed pseudo-evolution to a **horse-like creature**.

## Brain Generation:
![IMG_2B480D5020CD-1](https://user-images.githubusercontent.com/120343561/220411380-6b2ea42c-117f-4dc5-a5ff-a5745487aae9.jpeg)

Figure 2: Robot Genetic Storage and Brain Synapse Construction

Source: Adapted from _Figure 6b: The phenotype "brain"..._ from [1]


The brain is made of a netowrk of synapses, connecting sensor and motor neurons of the creature.
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

## The Parallel Hill Climber

## References:
Sims, Karl. “Evolving 3D Morphology and Behavior by Competition.” Artificial Life, vol. 1, no. 4, 1994, pp. 353–372., https://doi.org/10.1162/artl.1994.1.4.353. 

## Results:

Insert graphs here



