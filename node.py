class Node:
    def __init__(self, isWall=False, reword=0, isFinish=False):
        self.rewords = [0, 0, 0, 0]
        self.isFinish = isFinish
        self.reword = reword
        self.isWall=isWall

    def setRewords(self,data:list):
        self.rewords=data

    def getMaxReword(self):
        if self.isFinish:
            return self.reword
        return max(self.rewords)

    def getMaxDirIndex(self):
        value = 0
        index = -1
        for i in range(len(self.rewords)):
            if self.rewords[i] > value:
                index = i
                self.rewords[i] = value
        return index

    def setReword(self, index, value):
        self.rewords[index] = value

class Wall(Node):
    def __init__(self):
        super().__init__(isWall=True)

class Goal(Node):
    def __init__(self, reword):
        super().__init__(reword=reword, isFinish=True)