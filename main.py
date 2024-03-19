import random as r
import numpy as np
import setting
import record
from node import *
from os import system
from time import sleep

node_map = [
    [Node(), Node(), Node(), Node(),Node(), Node(), Node(),Node(), Node(), Goal(255)],
    [Node(), Node(), Node(), Node(),Node(), Node(), Node(),Wall(), Node(), Node()],
    [Node(), Node(), Node(), Node(),Node(), Node(), Node(),Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(),Wall(), Node(), Node(),Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(),Wall(), Node(), Node(),Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(),Node(), Node(), Node(),Node(), Node(), Wall()],
    [Node(), Node(), Node(), Node(),Node(), Node(), Node(),Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(),Wall(), Node(), Node(),Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(),Wall(), Node(), Node(),Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(),Wall(), Node(), Node(),Node(), Node(), Goal(25)]
]

pos = [0, 0]
last_dir = [0, 0]
action_count = 0
count_list = []
epochs = 0

direction = [
    [0, 1],
    [1, 0],
    [0, -1],
]


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
            node_map[i][j].setRewords(record[i][j])

def saveData(data):
    text="data=[\n"
    for i in range(len(data)):
        text+="["
        for j in range(len(data[i])):
            text+=f"{data[i][j].rewords}, "
        text+="],\n"
    text+="]"
    f=open("record.py","w")
    f.writelines(text)
    f.close()
    return text

def displayResult():
    text = "\n"
    for i in range(len(node_map)):
        for j in range(len(node_map[i])):
            temp = node_map[i][j].getMaxDirIndex()
            if temp != -1:
                text += "↓→↑"[temp]
            else:
                if node_map[i][j].isFinish:
                    text += str(node_map[i][j].reword)
                else:
                    text += "□"
            text += " "
        text += "\n"
    print(text)

def getDir(pos) -> list:
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
                    text+="※"
                else:
                    text+="□"
            if node_map[i][j].isFinish:
                text += f"{node_map[i][j].reword}"
            else:
                text += " "#str(node_map[i][j].rewords) + "    \t"
        text += "\n"
    print(text)
    print(f"pos : {pos}\tdir : {last_dir}\tcnt : {action_count}   \tepc : {epochs}")
    count_average = 0
    if count_list != []:
        count_average = np.round(sum(count_list) / len(count_list), 1)
    print(f"ctA : {count_average}")


def epsilonGreedy() -> bool:
    return r.random() < setting.epsilon


def execute():
    global pos, last_dir, action_count
    _node = node_map[pos[1]][pos[0]]

    # 다음 위치 선정
    _max_Q_dir_index = _node.getMaxDirIndex()
    if _max_Q_dir_index == -1 or epsilonGreedy():
        _dir = getDir(pos)
        _dir = _dir[r.randint(0, len(_dir) - 1)]
    else:
        _dir = direction[_max_Q_dir_index]
    _next = add(pos, _dir)

    # 연산할 값 선언
    _next_node = node_map[_next[1]][_next[0]]
    Q = _next_node.getMaxReword()
    last_dir = _dir
    action_count += 1

    if Q == 0:
        pos = _next
        return 0
    else:
        index = getDirIndex(_dir)
        pos = _next
        if _next_node.isFinish:
            _node.setReword(index, Q)
            return 1
        _node.setReword(index, np.round(Q * setting.gamma, 4))
        return 0

def Log(title, content):
    print(f"[ {title} ] >> {content}")


def fit_withoutDebug():
    global epochs
    while True:
        result=execute()
        if result:
            epochs += 1
            print(epochs)
            return

def fit():
    global epochs
    while True:
        system("cls")
        result=execute()
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
Log("system","start simulator")
sleep(1)
for i in range(setting.epochs_length):
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