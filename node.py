from time import sleep


class Node:
    def __init__(self, isWall=False, reword=0, isFinish=False):
        self.Qvalues = [0.0, 0.0, 0.0, 0.0]
        self.isFinish = isFinish
        self.reword = reword
        self.isWall = isWall

    def setQvalues(self, data: list):
        self.Qvalues = data

    def getMaxReword(self):
        if self.isFinish:
            return self.reword
        return max(self.Qvalues)

    def getMaxDirIndex(self, isReturnValue=False) -> list:
        value = 0
        same_value_indexes = []
        for i in range(len(self.Qvalues)):
            if self.Qvalues[i] == value:
                same_value_indexes.append(i)
            if self.Qvalues[i] > value:
                same_value_indexes = [i]
                value = self.Qvalues[i]
        if isReturnValue:
            return (same_value_indexes, value)
        return same_value_indexes

    def setReword(self, index, value):
        self.Qvalues[index] = value


class Wall(Node):
    def __init__(self):
        super().__init__(isWall=True)


class Goal(Node):
    def __init__(self, reword):
        super().__init__(reword=reword, isFinish=True)
