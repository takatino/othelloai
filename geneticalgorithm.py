import numpy
import math

class Population():
    def __init__(self, popsize, nn):
        self.popsize = popsize
        self.nn = nn
        self.population = []
        self.generation = 0

        for i in range(popsize):
            nn.weights, nn.biases = nn.scramble()
            self.population.append([numpy.random.randint(0, 100), nn.weights, nn.biases]) #[[fitness, weights, biases], ...]

    #orders population by score(highest to lowest), then normalizes that score    
    def rank(self):
        self.population.sort(key=takeFirst, reverse=True)

    def naturalselection(self, toppercent, breedpercent, mutationRate): #be careful with population size and toppercent, breedpercent:
        newpopulation = []                                #there can be instances where the selectedpopulation is too small to breed
        selectedpopulation = []
        #first, choose top% of population
        for i in range(math.floor(self.popsize * toppercent)):
            selectedpopulation.append(self.population[i])
            newpopulation.append(self.population[i])

        #next, breed for breed% of population
        totalscore = 0
        for i in range(len(selectedpopulation)):
            totalscore += selectedpopulation[i][0]
        for i in range(len(selectedpopulation)):
            selectedpopulation[i][0] /= totalscore
        for i in range(len(selectedpopulation)):
            if i == 0:
                continue
            else:
                selectedpopulation[i][0] += selectedpopulation[i-1][0]

        for i in range(math.floor(self.popsize * breedpercent)):
            selector = numpy.random.uniform(0, 1)
            for j in range(len(selectedpopulation)):
                if j == 0 and selector <= selectedpopulation[0][0]:
                    parentA = selectedpopulation[0]
                    parentAindex = j
                    break
                elif selectedpopulation[j-1][0] < selector and selector <= selectedpopulation[j][0]:
                    parentA = selectedpopulation[j]
                    parentAindex = j
                    break

            parentBindex = -1
            while parentAindex == parentBindex or parentBindex == -1:
                selector = numpy.random.uniform(0, 1)
                for j in range(len(selectedpopulation)):
                    if j == 0 and selector <= selectedpopulation[0][0]:
                        parentB = selectedpopulation[0]
                        parentBindex = j
                        break

                    elif selectedpopulation[j-1][0] < selector and selector <= selectedpopulation[j][0]:
                        parentB = selectedpopulation[j]
                        parentBindex = j
                        break

            baby = [0, self.nn.scramble()[0], self.nn.scramble()[1]]
            
            splicing = round(numpy.random.uniform(0, 1)) #0 -> parentA dna, 1 -> parenB dna
            for i in range(len(baby[1])):
                for r in range(len(baby[1][i])):
                    for c in range(len(baby[1][i][r])):

                        if numpy.random.uniform(0, 1) < mutationRate: #mutation!
                            baby[1][i][r][c] = numpy.random.randn()

                        if splicing == 0:
                            baby[1][i][r][c] = parentA[1][i][r][c]
                        elif splicing == 1:
                            baby[1][i][r][c] = parentB[1][i][r][c]

                        if numpy.random.uniform(0, 1) < 0.2:
                            if splicing == 0:
                                splicing = 1
                            elif splicing == 1:
                                splicing = 0
            
            splicing = round(numpy.random.uniform(0, 1))
            for i in range(len(baby[2])):
                for r in range(len(baby[2][i])):
                    for c in range(len(baby[2][i][r])):
                        
                        if numpy.random.uniform(0, 1) < mutationRate: #mutation!
                            baby[2][i][r][c] = numpy.random.randn()

                        if splicing == 0:
                            baby[2][i][r][c] = parentA[2][i][r][c]
                        elif splicing == 1:
                            baby[2][i][r][c] = parentB[2][i][r][c]

                        if numpy.random.uniform(0, 1) < 0.2:
                            if splicing == 0:
                                splicing = 1
                            elif splicing == 1:
                                splicing = 0

            newpopulation.append(baby)

        #add completely new population
        for i in range(len(newpopulation), self.popsize):
            baby = [0, self.nn.scramble()[0], self.nn.scramble()[1]]
            newpopulation.append(baby)

        self.generation += 1
        return newpopulation

#used to sort element by 0th item
def takeFirst(elem):
    return elem[0]