import numpy as np
from copy import deepcopy

class Matrix:
    def __init__(self, row, col, wincount):

        self.row = row
        self.col = col
        self.wincount = wincount
        self.buffer = np.matrix(
            [['-' for _ in range (col)] for _ in range (row)]
        )
        self.turn = 'X'
    def isOccupied(self, i, j):
        return self.buffer[i, j] != '-'
    def add(self, i, j):
        if (not self.isOccupied(i, j)):
            if (self.turn == 'X'):
                self.buffer[i, j] = 'X'
                self.turn = 'O'
            else:
                self.buffer[i, j] = 'O'
                self.turn = 'X'

    def clear(self):
        for i in range (self.row):
            for j in range (self.col):
                self.buffer[i, j] = '-'
        self.turn = 'X'

    def getLineIndexes(i, j, row, col, length):
        retList = []
        tupleList = []
        


        # horizontal
        lowest = max(0, j-length+1)
        highest = min(col-length, j+length-1)
        for n in range(lowest, highest+1):
            tupleList = []
            for m in range(length):
                tupleList.append((i, n+m))
            if len(tupleList) != 0:
                retList.append(tupleList)

        # vertical
        lowest = max(0, i-length+1)
        highest = min(row-length, i+length-1)
        for n in range(lowest, highest+1):
            tupleList = []
            for m in range(length):
                tupleList.append((n+m, j))
            if len(tupleList) != 0:
                retList.append(tupleList)
        
        # diagonal topleft-bottomright
        for offset in range(1-length, length):
            tupleList = []
            for m in range(length):
                idx_i = i+offset+m
                idx_j = j+offset+m
                if (idx_i >= 0 and idx_i < row and idx_j >= 0 and idx_j < col):
                    tupleList.append((idx_i, idx_j))
                else:
                    tupleList = []
                    break
            if len(tupleList) != 0:
                retList.append(tupleList)
        
        # diagonal topright-bottomleft
        for offset in range(1-length, length):
            tupleList = []
            for m in range(length):
                idx_i = i+offset-m
                idx_j = j-offset+m
                if (idx_i >= 0 and idx_i < row and idx_j >= 0 and idx_j < col):
                    tupleList.append((idx_i, idx_j))
                else:
                    tupleList = []
                    break
            if len(tupleList) != 0:
                retList.append(tupleList)


        return retList

    def hashLine(line):
        str = ""
        for i in line:
                str += f"{i[0]:02d}"
                str += f"{i[1]:02d}"
        return str    


    def calculate(self):

        X_points = 0
        O_points = 0

        ## 8 line

        # indexes = [
        #     # horizontal
        #     [(0,0), (0,1), (0,2)],
        #     [(1,0), (1,1), (1,2)],
        #     [(2,0), (2,1), (2,2)],

        #     # vertical
        #     [(0,0), (1,0), (2,0)],
        #     [(0,1), (1,1), (2,1)],
        #     [(0,2), (1,2), (2,2)],

        #     # diagonal
        #     [(0,0), (1,1), (2,2)],
        #     [(2,0), (1,1), (0,2)]
        # ]
        MAXPOINTS = 10**(self.wincount-1)
        MINPOINTS = -MAXPOINTS
        row = self.row
        col = self.col
        length = self.wincount
        accessedLine = set()
        indexes = []
        for i in range(row):
            for j in range(col):
                if (self.buffer[i,j] != '-'):
                    lines = (Matrix.getLineIndexes(i, j, row, col, length))
                    for line in lines:
                        hashed_line = Matrix.hashLine(line)
                        if hashed_line not in accessedLine:
                            accessedLine.add(hashed_line)
                            indexes += [line]


        for line in indexes:
            XCount = 0
            OCount = 0
            for idx in line:
                char = self.buffer[idx]
                if char == 'X':
                    XCount += 1
                elif char == 'O':
                    OCount += 1
            if (XCount == self.wincount):
                return MAXPOINTS
            elif (OCount == self.wincount):
                return MINPOINTS
            elif (XCount != 0 and OCount == 0):
                X_points += 10**(XCount-1)

            elif (XCount == 0 and OCount != 0):
                O_points += 10**(OCount-1)
        return X_points - O_points

class TreeMat:
    def __init__(self, matrix, maxdepth):
        self.matrix = matrix
        self.maxdepth = maxdepth
        self.children = []
        self.turns = 0
        self.noExpand = False
        self.cost = 0
    def generateMoves(self):
        if not self.noExpand:
            if (len(self.children) == 0):
                for i in range (self.matrix.row):
                    for j in range (self.matrix.col):
                        if not self.matrix.isOccupied(i, j):
                            # empty
                            cpyMat = deepcopy(self.matrix)
                            cpyMat.add(i, j)
                            newTree = TreeMat(cpyMat, self.maxdepth)
                            newTree.turns = self.turns+1
                            newTree.lastMove = (i, j)
                            self.children.append(newTree)
                    
    
    def setCostAndExpand(self, currentDepth):
        MAXPOINTS = 10**(self.matrix.wincount-1)
        MINPOINTS = -MAXPOINTS
        points = self.matrix.calculate()
        # self.cost = points
        # one side win
        if (points == MAXPOINTS or points == MINPOINTS):
            self.noExpand = True
            self.cost = points
            return

        # draw end
        if (self.turns == self.matrix.row*self.matrix.col):
            self.noExpand = True
            self.cost = 0
            return

        
        if (currentDepth < self.maxdepth):
        ## keep expanding
            self.generateMoves()
            if (len(self.children) != 0):
                maxVal = MINPOINTS
                minVal = MAXPOINTS
                maxNode = None
                minNode = None
                for i in range(len(self.children)):
                    child = self.children[i]
                    child.setCostAndExpand(currentDepth+1)
                    value = child.cost
                    child.noExpand = True
                    if (value > maxVal):
                        maxVal = value
                        if maxNode != None:
                            maxNode.noExpand = True
                        maxNode = child
                        child.noExpand = False
                    if (value < minVal):
                        minVal = value
                        if minNode != None:
                            minNode.noExpand = True
                        minNode = child
                        child.noExpand = False
                self.children.sort(key=lambda x: x.cost, reverse=True) ## always sorted
                
                ## maximizer or minimizer
                if self.matrix.turn == 'X':
                    # maximizer
                    self.cost = maxVal
                    return
                else:
                    self.cost = minVal
                    return
            else:
                # dont have legal move
                self.cost = points
                return
        else:
            self.cost = points
            return
        