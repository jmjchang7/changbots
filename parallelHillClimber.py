from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np
import matplotlib.pyplot as plt

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.fitnessValues = np.empty([c.numberOfGenerations+1, c.populationSize])
        self.currentGeneration = 0
        self.nextAvailableID = 0
        for key in range(c.populationSize):
            self.parents[key] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        self.Evaluate(self.parents)
        self.Store_Fitness()
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()
        self.Store_Fitness()

    def Spawn(self):
        self.children = {}
        for key in self.parents:
            self.children[key] = copy.deepcopy(self.parents[key])
            self.children[key].Set_ID(self.nextAvailableID) 
            self.nextAvailableID += 1

    def Mutate(self):
        for key in self.children:
            self.children[key].Mutate()

    def Select(self):
        for key in self.parents:
            if abs(self.parents[key].fitness) < abs(self.children[key].fitness):
                self.parents[key] = self.children[key]

    def Store_Fitness(self):
        for key in self.parents:
            self.fitnessValues[self.currentGeneration][key] = self.parents[key].fitness
        self.currentGeneration += 1

    def Print(self):
        print("\n")
        for key in self.parents:
            print("Parent fitness: " + str(self.parents[key].fitness) + ", Child fitness: " + str(self.children[key].fitness))
        print("\n")

    def Show_Best(self):
        max = self.parents[0].fitness
        maxKey = 0
        for key in self.parents:
            if abs(self.parents[key].fitness) > max:
                max = self.parents[key].fitness
                maxKey = key
        
        self.parents[maxKey].Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT")
        
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()

    def Get_Fitness_Curve(self):
        self.fitnessValues = abs(self.fitnessValues)
        return np.max(self.fitnessValues, axis=1)

    def Plot_Fitness_Curves(self):
        print(self.fitnessCurves)
        for i in range(c.numSeeds):
            plt.plot(range(c.numberOfGenerations+1), self.fitnessCurves[i], label='Seed ' + str(i + 1))

        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Evolution Curves')

        plt.legend()
        plt.show()
        plt.savefig('curve.png')