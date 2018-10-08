import random
from threading import Thread
from src import Chromosome


class GeneticProgram(Thread):
    currBest = None
    observers = None
    keepFittest = False
    mutationChancePercent = 0.1
    crossOverChance = 0.9
    genePoolSize = 40
    tournamentSize = 5
    maximumAmountOfGenerations = 0
    running = True
    selectionType = 0

    def __init__(self, observer):
        Thread.__init__(self)
        self.observers = observer

    def generateInitialGenePool(self, popSize):
        pool = []
        for i in range(0, popSize):
            tempChromo = Chromosome.ImageChromosome()
            tempChromo.random()
            tempChromo.calculateFitness()
            pool.append(tempChromo)

        return pool

    def _notify(self, args):
        self.observers.update(args)

    def run(self):
        currPool = self.generateInitialGenePool(int(self.genePoolSize))
        currPool.sort(key=lambda x: x.fitnessVal)
        self.currBest = currPool[0]
        count = 0
        while self.running:
            self.observers.root.update()
            parent1 = None
            parent2 = None
            nextGen = []
            if self.maximumAmountOfGenerations != 0 and self.maximumAmountOfGenerations == count:
                self.running = False

            if len(currPool) > 1:
                if random.uniform(0, 1) <= self.crossOverChance:
                    parent1, parent2 = self.parentSelection(self.selectionType, currPool)
                    child1, child2 = parent1.twoPointCrossover(parent2)
                    nextGen.append(child1)
                    nextGen.append(child2)

            if self.keepFittest:
                nextGen.append(currPool[0])

            for v in currPool:
                if v != parent1 or v != parent2:
                    if self.keepFittest:
                        if v != currPool[0]:
                            if random.uniform(0, 1) <= self.mutationChancePercent:
                                nextGen.append(v.mutation())
                            else:
                                nextGen.append(v)
                    else:
                        if random.randint(0, 1) <= self.mutationChancePercent:
                            nextGen.append(v.mutation())
                        else:
                            nextGen.append(v)

            nextGen.sort(key=lambda x: x.fitnessVal)

            while len(nextGen) > self.genePoolSize:
                nextGen.pop()

            currPool = []
            currPool.extend(nextGen)
            print(str(currPool[0].getFitnessVal()) + "best fitness in pool")
            self.setCurrentBest(currPool[0])

            count += 1

    def tournamentSelection(self, pop, size):
        best = None
        par2 = None
        par1 = None
        for x in range(size):
            v = random.randint(0, len(pop) - 1)
            curr = pop[v]
            if best == None or curr.fitnessVal < best.fitnessVal:
                best = curr
        par1 = best
        pop.remove(par1)  # remove so can't be picked again

        for x in range(size):
            curr = pop[random.randint(0, len(pop) - 1)]
            if best == None or curr.fitnessVal < best.fitnessVal:
                best = curr
        par2 = best
        pop.append(par1)
        return par1, par2

    def setCurrentBest(self, newBest):
        self.currBest = newBest
        img = newBest.createImage()
        self._notify(img)

    def rouletteSelection(self, population):
        par1 = None
        par2 = None
        val = 0
        totalFitness = 0
        maxFitness = population[len(population) - 1].getFitnessVal()
        count = 0

        for x in population:
            totalFitness += maxFitness - x.getFitnessVal()
        val = random.uniform(0, totalFitness)
        sum = 0
        count = 0
        while sum < val:
            sum += maxFitness - population[count].getFitnessVal()
            if sum < val:
                count += 1
        par1 = population[count]

        repeat = True
        while repeat:
            val = random.uniform(0, totalFitness)
            sum = 0
            count = 0
            while sum < val:
                sum += maxFitness - population[count].getFitnessVal()
                if sum < val:
                    count += 1
            par2 = population[count]
            if par2 != par1:
                repeat = False
        return par1, par2

    def parentSelection(self, type, pop):
        par1 = None
        par2 = None
        if type == 0:
            par1, par2 = self.tournamentSelection(pop, self.tournamentSize)
        if type == 1:
            par1, par2 = self.rouletteSelection(pop)

        return par1, par2

    def stop(self):
        self.running = False
        self.observers.startStopButton.configure(text="Start")
        self.observers.startStopButton.configure(command=self.observers.startGenetic)
        self.observers.enableAll()
        self.observers.enableSave()
