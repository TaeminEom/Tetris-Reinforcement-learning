import copy

global SIZE, figure, width, height

SIZE = [10, 20]
SMALLSIZE = [4, 20]
PIXEL = 20

red = (255, 174, 201)
blue = (0, 255, 255)
green = (128, 255, 0)
yellow = (255, 255, 128)
purple = (200, 150, 255)
orange = (255, 170, 130)
navy = (140, 140, 255)

"""figure = [[[[1, 1, 1, 1]], [[1], [1], [1], [1]]], [[[1, 1], [1, 1]]], [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]],
          [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]], [[[0, 1], [0, 1], [1, 1]], [[1, 1], [1, 0], [1, 0]],
          [[1, 0, 0], [1, 1, 1]], [[1, 1, 1], [0, 0, 1]]], [[[1, 0], [1, 0], [1, 1]], [[1, 1], [0, 1], [0, 1]],
          [[0, 0, 1], [1, 1, 1]], [[1, 1, 1], [1, 0, 0]]], [[[1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 1]],
          [[1, 0], [1, 1], [1, 0]], [[0, 1], [1, 1], [0, 1]]]]"""

blockMap = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
figure = [[[[navy, navy, navy, navy]], [[navy], [navy], [navy], [navy]]],
        [[[red, red], [red, red]]],
        [[[blue, blue, 0], [0, blue, blue]], [[0, blue], [blue, blue], [blue, 0]]],
        [[[0, green, green], [green, green, 0]], [[green, 0], [green, green], [0, green]]],
        [[[0, yellow], [0, yellow], [yellow, yellow]], [[yellow, yellow], [yellow, 0], [yellow, 0]], [[yellow, 0, 0], [yellow, yellow, yellow]], [[yellow, yellow, yellow], [0, 0, yellow]]],
        [[[purple, 0], [purple, 0], [purple, purple]], [[purple, purple], [0, purple], [0, purple]], [[0, 0, purple], [purple, purple, purple]], [[purple, purple, purple], [purple, 0, 0]]],
        [[[orange, orange, orange], [0, orange, 0]], [[0, orange, 0], [orange, orange, orange]],  [[orange, 0], [orange, orange], [orange, 0]], [[0, orange], [orange, orange], [0, orange]]]]
height = [[4, 1], [2], [3, 2], [3, 2], [2, 2, 3, 3], [2, 2, 3, 3], [3, 3, 2, 2]]
width = [[1, 4], [2], [2, 3], [2, 3], [3, 3, 2, 2], [3, 3, 2, 2], [2, 2, 3, 3]]
setHeight = [[[1], [1, 1, 1, 1]], [[1, 1]], [[1, 0], [0, 1, 1]], [[0, 1], [1, 1, 0]], [[0, 0, 1], [1, 1, 1], [1, 1], [1, -1]],
             [[1, 1, 1], [1, 0, 0], [-1, 1], [1, 1]], [[1, 0], [0, 1], [1, 1, 1], [0, 1, 0]]]


def findDistanceFromWall(x):
    if x <= 3:
        x += 1
        return 4 / x
    if x >= 7:
        x = SIZE[0] - x
        return 4 / x
    return 1

def simplifyMap(blockMap):
    simplifiedMap = []
    size = [len(blockMap), len(blockMap[0])]
    for i in range(size[0]):
        for j in reversed(range(size[1])):
            if blockMap[i][j] != 0:
                simplifiedMap.append(j)
                break
            elif j == 0:
                simplifiedMap.append(-1)
    minNum = min(simplifiedMap)
    for i in range(SMALLSIZE[0]):
        simplifiedMap[i] -= minNum + 1
    return simplifiedMap

def subSimplifyMap(blockMap):
    simplifiedMap = []
    smallSize = [len(blockMap), len(blockMap[0])]
    for i in range(smallSize[0]):
        for j in reversed(range(smallSize[1])):
            if blockMap[i][j] != 0:
                simplifiedMap.append(j)
                break
            if j == 0:
                simplifiedMap.append(-1)
    return simplifiedMap

def findSetBlockHeight(subSimplifiedMap, figureNum, x):
    setBlockHeight = []
    for i in range(width[figureNum[0]][figureNum[1]]):
        setBlockHeight.append(subSimplifiedMap[x + i] + setHeight[figureNum[0]][figureNum[1]][i])
    return max(setBlockHeight)

def setBlock(blockMap, figureNum, x):
    blockMap = copy.deepcopy(blockMap)
    subSimplifiedMap = subSimplifyMap(blockMap)
    setBlockHeight = findSetBlockHeight(subSimplifiedMap, figureNum, x)
    for i in range(width[figureNum[0]][figureNum[1]]):
        for j in range(height[figureNum[0]][figureNum[1]]):
            if figure[figureNum[0]][figureNum[1]][i][j] != 0:
                blockMap[x + i][setBlockHeight + j] = figure[figureNum[0]][figureNum[1]][i][j]
    return blockMap

def clearLine(blockMap):
    blockMap = copy.deepcopy(blockMap)
    for i in reversed(range(SIZE[1])):
        for j in range(SIZE[0]):
            if blockMap[j][i] == 0:
                break
            if j == SIZE[0]-1:
                for k in range(i, SIZE[1] - 1):
                    for l in range(SIZE[0]):
                        blockMap[l][k] = blockMap[l][k + 1]
                for k in range(SIZE[0]):
                    blockMap[k][SIZE[1]-1] = 0
    return blockMap

def existIn(list, one, location):
    try:
        return list[location[0]][location[1]][location[2]].index(one)
    except ValueError:
        return -1

def setReward(oneReward):
    sum = 0
    for i, j in zip(reversed(oneReward), range(len(oneReward))):
        sum += i * (0.9) ** j
    if len(oneReward) == 0:
        return 0
    return sum / (10 * (1 - 0.9 ** len(oneReward)))

def setSubReward(rewardRubble):
    # 0.6 0.24 0.096 0.0384 0.01536
    # 0.8 0.16 0.132 0.0064 0.00128
    rewardSum = 0
    rewardSum += 1 * rewardRubble[0]
    """
    rewardSum += 0.24 * rewardRubble[1]
    rewardSum += 0.096 * rewardRubble[2]
    rewardSum += 0.0384 * rewardRubble[3]
    rewardSum += 0.01536 * rewardRubble[4]"""
    return rewardSum

def checkHole(blockMap):
    count = 0
    size = [len(blockMap), len(blockMap[0])]
    for i in range(size[0]):
        for j in range(size[1]-1):
            if blockMap[i][j] == 0 and blockMap[i][j + 1] != 0:
                count += 1
    return count

def findMean(simplifiedMap):
    return sum(simplifiedMap) / len(simplifiedMap)

def findStandardDeviation(simplifiedMap):
    mean = findMean(simplifiedMap)
    deviation = []
    for i in simplifiedMap:
        deviation.append((i - mean) ** 2)
    standardDeviation = (sum(deviation) / len(simplifiedMap)) ** 0.5
    return standardDeviation

def countClearLine(blockMap):
    clearLineCount = 0
    for i in reversed(range(SIZE[1])):
        for j in range(SIZE[0]):
            if blockMap[j][i] == 0:
                break
            if j == SIZE[0] - 1:
                clearLineCount += 1
    return clearLineCount

def findHeightDifferenceMean(simplifiedMap):
    mean = 0
    for i in range(len(simplifiedMap) - 1):
        mean += abs(simplifiedMap[i] - simplifiedMap[i+1])
    return mean / (len(simplifiedMap) - 1)

def grade(blockMap, tempI):
    blockMap = copy.deepcopy(blockMap)
    smallBlockMap = copy.deepcopy(blockMap[tempI:tempI + 4])
    smallSimplifiedMap = subSimplifyMap(smallBlockMap)

    heightDifferenceMean = findHeightDifferenceMean(smallSimplifiedMap)
    standardDeviationChange = findStandardDeviation(smallSimplifiedMap)
    sumSimplifiedMap = sum(smallSimplifiedMap)
    reward = (-1) * (standardDeviationChange + heightDifferenceMean + 6 * sumSimplifiedMap)
    return reward