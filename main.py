from Tetris import *
import pygame as pg
import random as rd
import keyboard
from statistics import median

print("z:가속하고 화면 출력하지 않기 : 더 빨라짐")
print("x:가속하기")
print("c:감속하기")

pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)

screen = pg.display.set_mode([SIZE[0] * PIXEL, SIZE[1] * PIXEL])

pg.display.set_caption("Tetris Learning Machine")

done = False


def draw(blockMap):
    screen.fill(GRAY)
    for i in range(SIZE[0]):
        for j in range(SIZE[1]):
            if blockMap[i][j] != 0:
                pg.draw.rect(screen, blockMap[i][j],
                             [i * PIXEL, PIXEL * SIZE[1] - (PIXEL * j) - PIXEL, PIXEL - 2, PIXEL - 2])
    pg.display.flip()


reward = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
situation = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
for i in range(21):
    for j in range(21):
        reward[i].append([])
        situation[i].append([])
        for k in range(21):
            reward[i][j].append([])
            situation[i][j].append([])

rewardSequence = [[], [], [], [], []]
numSequence = [-1, -1, -1, -1, -1]
locationSequence = [-1, -1, -1, -1, -1]
roundNum = 0
speed = 1

a = []

print("", end="")
while not done:
    event = pg.event.poll()  # 이벤트 처리
    if event.type == pg.QUIT:
        break
    roundNum += 1
    tempRewardDifference = -100
    count = 0
    figureNum = [rd.randrange(0, len(figure)), 0]
    try:
        for k in range(len(figure[figureNum[0]])):
            figureNum[1] = k
            for i in range(SIZE[0] + 1 - 4):
                nowSimplifiedMap = subSimplifyMap(blockMap[i:i + 4])
                nowLocation = [nowSimplifiedMap[0] + 1, nowSimplifiedMap[1] + 1, nowSimplifiedMap[2] + 1]
                nowSituationNum = existIn(situation, nowSimplifiedMap, nowLocation)
                nowReward = 0
                if nowSituationNum != -1:
                    nowReward = setReward(reward[nowLocation[0]][nowLocation[1]][nowLocation[2]][nowSituationNum])
                for j in range(4 + 1 - width[figureNum[0]][figureNum[1]]):
                    x = i + j
                    newMap = setBlock(blockMap, figureNum, x)
                    simplifiedMap = subSimplifyMap(newMap[i:i + 4])
                    location = [simplifiedMap[0] + 1, simplifiedMap[1] + 1, simplifiedMap[2] + 1]
                    situationNum = existIn(situation, simplifiedMap, location)

                    if situationNum == -1:
                        count += 1
                        if tempRewardDifference < 0:
                            tempReward = 0
                            tempNum = len(situation[location[0]][location[1]][location[2]])
                            tempMap = copy.deepcopy(newMap)
                            tempI = i
                            tempRewardDifference = 0
                            tempLocation = copy.deepcopy(location)
                        weight = findDistanceFromWall(x)
                        percent = weight / count  # 1 / count * weight
                        if tempRewardDifference == 0 and rd.random() < percent:
                            tempNum = len(situation[location[0]][location[1]][location[2]])
                            tempMap = copy.deepcopy(newMap)
                            tempI = i
                            tempRewardDifference = 0
                            tempLocation = copy.deepcopy(location)
                    elif tempRewardDifference < setReward(reward[location[0]][location[1]][location[2]][situationNum]) - nowReward:
                        tempReward = setReward(reward[location[0]][location[1]][location[2]][situationNum])
                        tempNum = situationNum
                        tempMap = copy.deepcopy(newMap)
                        tempI = i
                        tempRewardDifference = tempReward - nowReward
                        tempLocation = copy.deepcopy(location)
                    if situationNum != -1:
                        if setReward(reward[location[0]][location[1]][location[2]][situationNum]) != 0 and nowReward != 0:
                            a.append(setReward(reward[location[0]][location[1]][location[2]][situationNum]) - nowReward)
                            print("a", median(a))

        if rd.random() < 0.01:
            figureNum[1] = rd.randrange(0, len(figure[figureNum[0]]))
            i = rd.randrange(0, SIZE[0] + 1 - 4)
            j = rd.randrange(0, 4 + 1 - width[figureNum[0]][figureNum[1]])
            x = i + j

            newMap = setBlock(blockMap, figureNum, x)
            simplifiedMap = subSimplifyMap(newMap[i:i + 4])
            location = [simplifiedMap[0] + 1, simplifiedMap[1] + 1, simplifiedMap[2] + 1]
            situationNum = existIn(situation, simplifiedMap, location)

            tempNum = len(situation[location[0]][location[1]][location[2]])
            if situationNum != -1:
                tempNum = situationNum
            tempMap = copy.deepcopy(newMap)
            tempI = i
            tempLocation = copy.deepcopy(location)
    except IndexError:
        if tempNum == len(situation[tempLocation[0]][tempLocation[1]][tempLocation[2]]):
            situation[tempLocation[0]][tempLocation[1]][tempLocation[2]].append(subSimplifyMap(tempMap[tempI:tempI + 4]))
            reward[tempLocation[0]][tempLocation[1]][tempLocation[2]].append([])

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
        for i in range(5):
            for j in range(5):
                rewardSequence[i].append(-10)
        numSequence[4] = tempNum
        locationSequence[4] = copy.deepcopy(tempLocation)

        for i in range(5):
            reward[locationSequence[i][0]][locationSequence[i][1]][locationSequence[i][2]][numSequence[i]].append(setSubReward(rewardSequence[i]))

        rewardSequence = [[], [], [], [], []]
        numSequence = [-1, -1, -1, -1, -1]
        locationSequence = [-1, -1, -1, -1, -1]

        if keyboard.is_pressed("z"):
            speed = 3
        if keyboard.is_pressed("x"):
            speed = 2
        if keyboard.is_pressed("c"):
            speed = 1
        if speed == 1:
            pg.time.delay(200)
            draw(blockMap)
        if speed == 2:
            draw(blockMap)

        sumLen = 0
        for i in range(21):
            for j in range(21):
                for k in range(21):
                    sumLen += len(situation[i][j][k])
        print("\r%d %d" % (roundNum, sumLen), end="")
        continue

    if tempNum == len(situation[tempLocation[0]][tempLocation[1]][tempLocation[2]]):
        situation[tempLocation[0]][tempLocation[1]][tempLocation[2]].append(subSimplifyMap(tempMap[tempI:tempI + 4]))
        reward[tempLocation[0]][tempLocation[1]][tempLocation[2]].append([])

    score = grade(tempMap, tempI)

    blockMap = copy.deepcopy(tempMap)
    blockMap = clearLine(blockMap)

    for i in range(5):
        rewardSequence[i].append(score)
    numSequence[4] = tempNum
    locationSequence[4] = copy.deepcopy(tempLocation)

    if numSequence[0] != -1:
        reward[locationSequence[0][0]][locationSequence[0][1]][locationSequence[0][2]][numSequence[0]].append(setSubReward(rewardSequence[0]))

    for i in range(4):
        rewardSequence[i] = rewardSequence[i + 1]
        numSequence[i] = numSequence[i + 1]
        locationSequence[i] = copy.deepcopy(locationSequence[i + 1])

    rewardSequence[4] = []
    numSequence[4] = -1
    locationSequence[4] = -1

    if keyboard.is_pressed("z"):
        speed = 3
    if keyboard.is_pressed("x"):
        speed = 2
    if keyboard.is_pressed("c"):
        speed = 1
    if speed == 1:
        pg.time.delay(200)
        draw(blockMap)
    if speed == 2:
        draw(blockMap)

    sumLen = 0
    for i in range(21):
        for j in range(21):
            for k in range(21):
                sumLen += len(situation[i][j][k])
    print("\r%d %d" % (roundNum, sumLen), end="")
pg.quit()
