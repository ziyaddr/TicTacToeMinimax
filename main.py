from itertools import count
import tkinter as tk
from tkinter import *
from tkinter import messagebox

from TicTacToe import Matrix
from TicTacToe import TreeMat
import numpy as np



class mainApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        ## variable
        self.rule = {
            'WINCOUNT': 3,
            'MAXPOINTS': 0,
            'MINPOINTS': 0,
            'MAXDEPTH': 3,
            'ROWCOUNT': 3,
            'COLCOUNT': 3,
            'LARGEFONT': ("Verdana", 20)
        }
        self.rule['MAXPOINTS'] = 10**(self.rule['WINCOUNT']-1)
        self.rule['MINPOINTS'] = -(10**self.rule['WINCOUNT']-1)

        self.boardFrame = tk.Frame(self, padx=10, pady=10)
        self.optionFrame = tk.Frame(self)
        self.boardFrame.grid(row=0, column=0)
        self.optionFrame.grid(row=0, column=1)
        self.boardMat = Matrix(self.rule['ROWCOUNT'], self.rule['COLCOUNT'], self.rule['WINCOUNT'])
        self.maxDepth = self.rule['MAXDEPTH']
        self.solutionTree = TreeMat(self.boardMat, self.maxDepth)
        self.solutionTree.setCostAndExpand(0)
        self.botX = False
        self.botO = True
        self.turnCount = 0
        
        self.createBoard(self.boardFrame)
        self.createOption(self.optionFrame)
        # self.changeRule(5, 5, 4, 2)
        self.autoMove()

    def createOption(self, parent):

        self.vr = StringVar()
        (Radiobutton(parent, text = "Play as X", variable = self.vr,
                value = "X").pack(side = TOP, ipady = 5))
        (Radiobutton(parent, text = "Play as O", variable = self.vr,
        value = "O").pack(side = TOP, ipady = 5))
        

        self.v_row = tk.StringVar()
        self.v_col = tk.StringVar()
        self.v_wincount = tk.StringVar()
        self.v_depth = tk.StringVar()
        tk.Label(parent, text = 'Row count=').pack()
        tk.Entry(parent, textvariable=self.v_row).pack()
        tk.Label(parent, text = 'Column count=').pack()
        tk.Entry(parent, textvariable=self.v_col).pack()
        tk.Label(parent, text = 'n-marks needed=').pack()
        tk.Entry(parent, textvariable=self.v_wincount).pack()
        tk.Label(parent, text = 'Max depth=').pack()
        tk.Entry(parent, textvariable=self.v_depth).pack()

        tk.Button(parent, text= "Reset and Apply", command = self.getVal).pack()

    def getVal(self):
        row = int(self.v_row.get())
        col = int(self.v_col.get())
        wincount = int(self.v_wincount.get())
        depth = int(self.v_depth.get())
        rb = (self.vr.get())
        if (rb == 'X'):

            autoX = False
            autoY = True
        else:
            autoX = True
            autoY = False
        
        self.changeRule(row, col, wincount, depth, autoX, autoY)

        self.autoMove()

    
    def createBoard(self, parent):
        self.blocks = np.matrix(
            [[None for _ in range (self.boardMat.col)] for _ in range (self.boardMat.row)]
        )
        for i in range (self.boardMat.row):
            for j in range (self.boardMat.col):
                self.blocks[i, j] = tk.Button(parent, text="  ", font=self.rule['LARGEFONT'], width=3, height=1, command= lambda i = i, j = j : self.addAction(i, j), borderwidth=4)
                self.blocks[i, j].grid(row=i, column=j, sticky=NSEW)
    
    def changeRule(self, row, col, wincount, maxdepth, autoX, autoY):
        self.rule['ROWCOUNT'] = row
        self.rule['COLCOUNT'] = col
        self.rule['WINCOUNT'] = wincount
        self.rule['MAXDEPTH'] = maxdepth
        self.rule['MAXPOINTS'] = 10**(wincount-1)
        self.rule['MINPOINTS'] = -(10**(wincount-1))
        self.boardFrame.destroy()
        self.boardFrame = tk.Frame(self, padx=10, pady=10)
        self.boardFrame.grid(row=0, column=0)

        self.boardMat = Matrix(row, col, wincount)
        self.solutionTree = TreeMat(self.boardMat, maxdepth)
        self.solutionTree.setCostAndExpand(0)
        self.botX = autoX
        self.botO = autoY
        self.turnCount = 0
        
        self.createBoard(self.boardFrame)


                
    def addAction(self, i, j):
        self.addAndRefresh(i, j)
        self.autoMove()

    def addAndRefresh(self, i, j):
        self.turnCount += 1
        self.boardMat.add(i, j)
        point = self.boardMat.calculate()
        self.refreshBoard()
        self.solutionTree.setCostAndExpand(0)
        for sol in self.solutionTree.children:
            if sol.lastMove == (i, j):
                self.solutionTree = sol
                self.solutionTree.noExpand = False
                break

        if (point == self.rule['MAXPOINTS'] or point == self.rule['MINPOINTS']):
            if point == self.rule['MAXPOINTS']:
                messagebox.showinfo(message="X WIN")
            else:
                messagebox.showinfo(message="O WIN")
            
            self.reset()
            self.solutionTree = TreeMat(self.boardMat, self.maxDepth)
            self.solutionTree.setCostAndExpand(0)
            
            self.turnCount = 0
            self.refreshBoard()
            self.autoMove()
            

            return
        if (self.turnCount == self.boardMat.row*self.boardMat.col):
            messagebox.showinfo(message="DRAW")
            
            self.reset()
            self.solutionTree = TreeMat(self.boardMat, self.maxDepth)
            self.solutionTree.setCostAndExpand(0)
            
            self.turnCount = 0
            
            self.refreshBoard()
            self.autoMove()
                
            return


    def reset(self):
        self.boardMat.clear()
        self.refreshBoard()
    
    def refreshBoard(self):
        for i in range (self.boardMat.row):
            for j in range (self.boardMat.col):
                char = self.boardMat.buffer[i, j]
                if (char != '-'):
                    self.blocks[i, j].config(text=char, command="")
                else:
                    self.blocks[i, j].config(text=' ', command= lambda i = i, j = j : self.addAction(i, j))
    
    def reset(self):
        self.boardMat.clear()

    def autoMove(self):
        
        if (self.boardMat.turn == 'X' and self.botX) or (self.boardMat.turn == 'O' and self.botO):

            if (len(self.solutionTree.children) != 0):
                if (self.boardMat.turn == 'X'):
                    lastMove = self.solutionTree.children[0].lastMove
                else:
                    lastMove = self.solutionTree.children[-1].lastMove
                self.addAndRefresh(lastMove[0], lastMove[1])
            else:
                self.solutionTree.setCostAndExpand(0)
                if (self.boardMat.turn == 'X'):
                    lastMove = self.solutionTree.children[0].lastMove
                else:
                    lastMove = self.solutionTree.children[-1].lastMove
                self.addAndRefresh(lastMove[0], lastMove[1])


if __name__ == "__main__":
    app = mainApp()
    app.mainloop()