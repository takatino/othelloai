from othello import *
from neuralnetwork import *
from geneticalgorithm import *
import numpy



#main game board
board = resetboard()

network1 = Network([64, 8, 8, 8, 64])
cpu1 = Population(40, network1)
network2 = Network([64, 8, 8, 8, 64])
cpu2 = Population(20, network2)
network3 = Network([64, 8, 8, 8, 64])
cpu3 = Population(40, network3)


cpu1id = 0
cpu2id = 0
cpu1.nn.load(cpu1.population[cpu1id][1], cpu1.population[cpu1id][2])
cpu2.nn.load(cpu2.population[cpu2id][1], cpu2.population[cpu2id][2])


scorecount = [0, 0, 0]

if numpy.random.uniform(0, 1) < 0.5:
    whoseTurn = 1
else:
    whoseTurn = -1


def loop():
    global board, whoseTurn, cpu1id, cpu2id

    if legalPlacements(board, 1) == [] and legalPlacements(board, -1) == []:
        reset()

    if legalPlacements(board, 1) == []:
        whoseTurn = -1
    if legalPlacements(board, -1) == []:
        whoseTurn = 1        
    
    if whoseTurn == 1: #white's turn
        input = []
        for r in range(8):
            for c in range(8):
                input.append([board[r][c]])

        output = cpu1.nn.feedforward(input)
        
        legalfilter = []
        for position in legalPlacements(board, 1):
            legalfilter.append(position[0] * 8 + position[1])

        for i in range(64):
            if i in legalfilter:
                pass
            else:
                output[i][0] = 0
        
        maxindex = numpy.argmax(output, axis = 0)[0]
        chosenr = int((maxindex - (maxindex % 8)) / 8)
        chosenc = int(maxindex % 8)

        placeDisk(board, 1, chosenr, chosenc)
        whoseTurn = -1
        

    elif whoseTurn == -1: #black's turn
        input = []
        for r in range(8):
            for c in range(8):
                input.append([-board[r][c]])

        output = cpu2.nn.feedforward(input)

        legalfilter = []
        for position in legalPlacements(board, -1):
            legalfilter.append(position[0] * 8 + position[1])

        for i in range(64):
            if i in legalfilter:
                pass
            else:
                output[i][0] = 0
        
        maxindex = numpy.argmax(output, axis = 0)[0]
        chosenr = int((maxindex - (maxindex % 8)) / 8)
        chosenc = int(maxindex % 8)

        placeDisk(board, -1, chosenr, chosenc)
        whoseTurn = 1



def reset():
    global board, whoseTurn, cpu1id, cpu2id, scorecount
 

    score = count(board)
    if score[0] > score[1]:
        cpu1.population[cpu1id][0] += 3
        scorecount[0] += 1
    elif score[0] < score[1]:
        cpu2.population[cpu2id][0] += 3
        scorecount[1] += 1
    else:
        cpu1.population[cpu1id][0] += 1
        cpu2.population[cpu2id][0] += 1
        scorecount[2] += 1

    cpu2id += 1
    if cpu2id == cpu2.popsize - 1 and cpu1id == cpu1.popsize - 1:
        print(scorecount)
        scorecount = [0, 0, 0]

        cpu2id = 0
        cpu1id = 0

        cpu1.rank()
        print(cpu1.generation, cpu1.population[0][0])
        cpu1.population = cpu1.naturalselection(0.3, 0.6, 0.1)
        cpu2.rank()
        cpu2.population = cpu2.naturalselection(0.3, 0.6, 0.1)

    elif cpu2id == cpu2.popsize - 1 and cpu1id < cpu1.popsize - 1:
        cpu2id = 0
        cpu1id += 1

    cpu1.nn.load(cpu1.population[cpu1id][1], cpu1.population[cpu1id][2])
    cpu2.nn.load(cpu2.population[cpu2id][1], cpu2.population[cpu2id][2])
    

    board = resetboard()
    if numpy.random.uniform(0, 1) < 0.5:
        whoseTurn = 1
    else:
        whoseTurn = -1



while True:
    loop()
