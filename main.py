import random as r
import numpy as np
import setting
from node import Node
from os import system
from time import sleep

node_map = [
    [Node(), Node(), Node(), Node(), Node(reword=5, isFinish=True)],
    [Node(), Node(), Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(), Node()],
    [Node(), Node(), Node(), Node(), Node(reword=25, isFinish=True)],
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
    elif nextPos[0] < 0 or nextPos[1] < 0:
        return True
    return False


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
                text += "="
            if node_map[i][j].isFinish:
                text += f"{node_map[i][j].reword}"
            else:
                text += str(node_map[i][j].rewords) + "    \t"
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
        if _next_node.isFinish:
            _node.setReword(index, Q)
            return 1
        _node.setReword(index, np.round(Q * setting.gamma, 4))
        pos = _next
        return 0


for i in range(setting.epochs_length):
    while True:
        system("cls")
        displayMap()
        if execute():
            # sleep(0.2)
            epochs += 1
            break
        # sleep(0.05)
    count_list.append(action_count)
    pos = [setting.start_pos[0], setting.start_pos[1]]
    last_dir = [0, 0]
    action_count = 0

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
                text += "_"
        text += " "
    text += "\n"
print(text)
