from solution import SOLUTION
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.parents = {}
        self.nextAvailableID = 0
        for key in range(c.populationSize):
            self.parents[key] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1


    def Evolve(self):
        self.Evaluate(self.parents)
        print('done')
        
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

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
            if self.parents[key].fitness > self.children[key].fitness:
                self.parents[key] = self.children[key]

    def Print(self):
        print("\n")
        for key in self.parents:
            print("Parent fitness: " + str(self.parents[key].fitness) + ", Child fitness: " + str(self.children[key].fitness))
        print("\n")

    def Show_Best(self):
        min = self.parents[0].fitness
        minKey = 0
        for key in self.parents:
            if self.parents[key].fitness < min:
                min = self.parents[key].fitness
                minKey = key
        
        self.parents[minKey].Start_Simulation("GUI")

    def Evaluate(self, solutions):
        for key in solutions:
            solutions[key].Start_Simulation("DIRECT")
        
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()