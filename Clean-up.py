import csv
import numpy as np
from sklearn.model_selection import train_test_split
import io
import os
import random
from sklearn.utils import shuffle

trainingSetPath = 'chessTrainingData.csv'
testSetPath = 'chessTestData.csv'
filePath = os.path.relpath('chessData.csv')


file = open(filePath)
csvreader = csv.reader(file)
header = []
header = next(csvreader)


boardStates = []
evaluations = []

for row in csvreader:
    boardStates.append(row[0])
    evaluations.append(row[1])

boardStates, evaluations = shuffle(boardStates, evaluations, random_state=1)

pieceDictionary = {'p': 1, 'r': 2, 'n': 3, 'b': 4, 'q': 5, 'k':6, 'P': -1, 'R': -2, 'N': -3, 'B': -4, 'Q': -5, 'K':-6}

playerDictionary = {'b': -1, 'w':1}


#Create a board matrix
def createBoardMatrix(fen):
    #Determine current player
    playerSplit = fen.split(' ')
    player = playerSplit[1]
    playerValue = playerDictionary[player]

    #Determine board layout
    pieceSplit = playerSplit[0].split('/')

    #Generate board matrix
    board = np.zeros((8, 8))
    rowPosition = 0
    for row in pieceSplit:
        colPosition = 0
        rowBreakDown = list(row)
        for value in rowBreakDown:
            if value.isalpha() == True:
                board[rowPosition, colPosition] = pieceDictionary[value]
                colPosition += 1
            else:
                colPosition += int(value)
        rowPosition += 1
    return board, playerValue

#Split board matrix into channels
def createChannel(board, piece):
    shape = board.shape
    channel = np.zeros((8, 8))

    for row in range(shape[0]):
        for col in range(shape[1]):
            if board[row, col] == piece:
                channel[row, col] = 1
            if board[row, col] == (-1* int(piece)):
                channel[row, col] = -1
    return channel

def channelToString(channel):
    shape = channel.shape
    value = ''
    for row in range(shape[0]):
        for col in range(shape[1]):
            value = value + str(channel[row, col]) + ' '
    return value

def onlyNumericalEvaluations(boardStates, evaluations):
    cleanBoardStates = []
    cleanEvaluations = []

    for i in range(len(evaluations)):
        evalBreakDown = list(evaluations[i])

        if evalBreakDown[0] != '#':
            cleanBoardStates.append(boardStates[i])
            cleanEvaluations.append(evaluations[i])
    return cleanBoardStates, cleanEvaluations

def createNumericalEvaluations(evaluations):
    numericEvaluations = []
    for eval in evaluations:
        numericalString = eval[1:] 
        numeric = 0

        evalBreadkown = list(eval)
        if evalBreadkown[0] == '+':
            numeric = int(numericalString)

        if evalBreadkown[0] == '-':
            numeric = -1 * int(numericalString)
        
        numericEvaluations.append(numeric)

    return numericEvaluations

   

###########################################
###########################################
#Translate
###########################################
###########################################

boardStates, evaluations = onlyNumericalEvaluations(boardStates, evaluations)
evaluations = createNumericalEvaluations(evaluations)

print(boardStates[0])
print(evaluations[0])

##########################################
#Determine training vs test split
dataSetSize = len(evaluations)
percentageSplit = 0.66
numberOfTrainingSamples = int(percentageSplit * dataSetSize)
numberOfTestSamples = int(dataSetSize - numberOfTrainingSamples)
print("dataset size: ", dataSetSize)
print("Number of training samples: ", numberOfTrainingSamples)
print("Number of test samples: ", numberOfTestSamples)
##########################################

##########################################
#Writing training and test files
fTrain = open(trainingSetPath, 'w')
trainWriter = csv.writer(fTrain)

fTest = open(testSetPath, 'w')
testWriter = csv.writer(fTest)
##########################################

##########################################
#Write csv headings
heading = ['pawnChannel', 'rookChannel', 'knightChannel', 'bishopChannel', 'queenChannel', 'kingChannel', 'playerChannel', 'evaluation']
trainWriter.writerow(heading)
testWriter.writerow(heading)
##########################################

sampleNumber = 0

#########
#DELETE
numberOfTrainingSamples = 10


for fen in boardStates[:20]:
    #Create channels
    board, player = createBoardMatrix(fen)
    pawnChannel = createChannel(board, 1)
    rookChannel = createChannel(board, 2)
    knightChannel = createChannel(board, 3)
    bishopChannel = createChannel(board, 4)
    queenChannel = createChannel(board, 5)
    kingChannel = createChannel(board, 6)
    playerChannel = np.full((8, 8), player)

    #channelsToString
    pawnString = channelToString(pawnChannel)
    rookString = channelToString(rookChannel)
    knightString = channelToString(knightChannel)
    bishopString = channelToString(bishopChannel)
    queenString = channelToString(queenChannel)
    kingString = channelToString(kingChannel)
    playerString = channelToString(playerChannel)
    sampleEvaluation = evaluations[sampleNumber]

    row = [pawnString, rookString, knightString, bishopString, queenString, kingString, playerString, sampleEvaluation]
    print("Sample: ", sampleNumber)

    if sampleNumber < numberOfTrainingSamples:
        trainWriter.writerow(row)
    else:
        testWriter.writerow(row)

    sampleNumber += 1

fTrain.close()
fTest.close()





        


