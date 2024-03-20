import random as r
import numpy as np
import setting
import record
from node import *
from os import system
from time import sleep

node_map = [
    [Node(),Node(), Wall(), Node(), Node(), Node(), Node(), Wall()],
    [Node(),Node(), Node(), Node(), Wall(), Node(), Node(), Node()],
    [Node(),Wall(), Wall(), Wall(), Node(), Node(), Node(), Node()],
    [Node(),Wall(), Node(), Node(), Node(), Node(), Node(), Node()],
    [Node(),Wall(), Node(), Node(), Node(), Node(), Wall(), Node()],
    [Node(),Wall(), Node(), Wall(), Node(), Node(), Node(), Node()],
    [Node(),Node(), Node(), Node(), Node(), Wall(), Node(), Goal(1)],
]

pos = [0, 0]
last_dir = [0, 0]
action_count = 0
count_list = []
epochs = 0

direction = [[0, 1], [1, 0], [0, -1], [-1, 0]]


def Log(title, content):
    print(f"[ {title} ] >> {content}")


def add(a: list, b: list) -> list:
    return [a[0] + b[0], a[1] + b[1]]


def isOverMap(pos, _dir) -> bool:
    nextPos = add(pos, _dir)
    if nextPos[0] >= len(node_map[0]) or nextPos[1] >= len(node_map):
        return True
    elif node_map[nextPos[1]][nextPos[0]].isWall:
        return True
    elif nextPos[0] < 0 or nextPos[1] < 0:
        return True
    return False


def loadData(record):
    global node_map
    for i in range(len(node_map)):
        for j in range(len(node_map[i])):
            node_map[i][j].setQvalues(record[i][j])


def saveData(data):
    text = "data=[\n"
    for i in range(len(data)):
        text += "["
        for j in range(len(data[i])):
            text += f"{data[i][j].Qvalues}, "
        text += "],\n"
    text += "]"
    f = open("record.py", "w")
    f.writelines(text)
    f.close()
    return text


def displayResult():
    text = "\n"
    for i in range(len(node_map)):
        for j in range(len(node_map[i])):
            temp, value = node_map[i][j].getMaxDirIndex(True)
            if temp != [] and value > 0:
                text += "↓→↑←"[temp[0]]
            else:
                if node_map[i][j].isFinish:
                    text += str(node_map[i][j].reword)
                else:
                    text += "□"
            text += " "
        text += "\n"
    print(text)


def getPossibleDir(pos) -> list:
    return [i for i in direction if not isOverMap(pos, i)]


def getDirIndex(_dir) -> int:
    for i in range(len(direction)):
        if direction[i] == _dir:
            return i
    return -1


def displayMap():
    text = ""
    for i in range(len(node_map)):
        for j in range(len(node_map[i])):
            if [j, i] == pos:
                text += "■"
            else:
                if node_map[i][j].isWall:
                    text += "※"
                else:
                    text += "□"
            if node_map[i][j].isFinish:
                text += f" {node_map[i][j].reword}"
            else:
                text += " "  # str(node_map[i][j].Qvalues) + "\t"
        text += "\n"
    print(text)
    print(f"pos : {pos}\tdir : {last_dir}\tcnt : {action_count}   \tepc : {epochs}")
    count_average = 0
    if count_list != []:
        count_average = np.round(sum(count_list) / len(count_list), 1)
    print(f"ctA : {count_average}")


def epsilonGreedy() -> bool:
    return r.random() < setting.epsilon


def QvalueUpdate(nowQ, R, maxQ):
    result = (1 - setting.alpha) * nowQ
    result += setting.alpha * (R + setting.gamma * maxQ)
    return np.round(result, 5)


last_distance = 16 * 2


def execute():
    global pos, last_dir, action_count, last_distance
    _node = node_map[pos[1]][pos[0]]

    # 다음 위치 선정
    _max_Q_dir_index = [direction[i] for i in _node.getMaxDirIndex()]
    _possible_dir = getPossibleDir(pos)
    _candidate_dir = [i for i in _max_Q_dir_index if i in _possible_dir]

    if epsilonGreedy() or _candidate_dir == []:
        # 입실론 그리디 or Max Q 방향에 벽 존재할 경우
        _dir = _possible_dir
        _dir = _dir[r.randint(0, len(_possible_dir) - 1)]
    else:
        _dir = _candidate_dir
        _dir = _dir[r.randint(0, len(_dir) - 1)]
    _next = add(pos, _dir)
    _next_node = node_map[_next[1]][_next[0]]

    # Q값 계산
    maxQ = _next_node.getMaxReword()
    _index = getDirIndex(_dir)
    nowQ = _node.Qvalues[_index]
    _distance = (_next[0] - 4) ** 2 + (_next[1] - 4) ** 2
    _reword = last_distance - _distance
    Q = QvalueUpdate(nowQ, 0, maxQ)

    # 기록
    last_dir = _dir
    action_count += 1
    last_distance = _distance

    _node.setReword(_index, Q)
    pos = _next
    if _next_node.isFinish:
        return 1
    # _node.setReword(index, np.round(Q * setting.gamma, 4))
    return 0


def fit_withoutDebug():
    global epochs
    while True:
        result = execute()
        if result:
            epochs += 1
            print(epochs)
            return


def fit():
    global epochs
    while True:
        system("cls")
        result = execute()
        displayMap()
        if result:
            sleep(0.2)
            epochs += 1
            break
        sleep(0.1)


# Main
if setting.isLoadData:
    Log("load", "import data...")
    loadData(record.data)
    Log("load", "complete")
    sleep(0.5)
Log("system", "start simulator")
sleep(1)
for i in range(setting.epochs_length):
    if setting.isLearnMode:
        fit_withoutDebug()
    else:
        fit()
    count_list.append(action_count)
    pos = [setting.start_pos[0], setting.start_pos[1]]
    last_dir = [0, 0]
    action_count = 0

print("\n\n\t[ Result ]\n")
if setting.isSaveData:
    saveData(node_map)
    print("[ Saved Data ]")
displayResult()

import matplotlib.pyplot as plt
import numpy as np
Log("result",sum(count_list)/len(count_list))
count_list = np.array(count_list).reshape(int(len(count_list)/8),8)
aver = [sum(i)/8 for i in count_list]
plt.plot(aver)
plt.show()