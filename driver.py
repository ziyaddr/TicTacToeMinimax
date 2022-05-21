from TicTacToe import TreeMat
from TicTacToe import Matrix
import numpy as np

# M = Matrix(3, 3)
# M.buffer = np.matrix(
# [
# ['-', '-', '-'],
# ['-', 'X', '-'],
# ['-', '-', '-']
# ]
# )
# M.turn = 'O'
# TM = TreeMat(M)
# TM.setCostAndExpand(0)
# print("---------")
# print(TM.cost)
# for child in TM.children:
#     print(child.matrix.buffer)
#     print(child.cost)
#     print(child.lastMove)
#     print("\n")
# print(TM.children[-1].lastMove)
# print(M.calculate())
# row = 4
# col = 4
# length = 4
# accessedLine = set()
# indexes = []
# for i in range(row):
#     for j in range(col):

#         lines = (Matrix.getLineIndexes(i, j, row, col, length))
#         for line in lines:
#             hashed_line = Matrix.hashLine(line)
#             if hashed_line not in accessedLine:
#                 accessedLine.add(hashed_line)
#                 indexes += [line]
# print(indexes)

M = Matrix(7, 6, 5)
M.buffer = np.matrix(
[
['-', '-', '-', '-', '-', '-'],
['-', '-', '-', '-', '-', '-'],
['-', '-', 'O', 'O', '-', '-'],
['-', 'X', 'X', 'X', 'X', '-'],
['-', '-', '-', 'O', '-', '-'],
['-', '-', '-', '-', '-', '-'],
['-', '-', '-', '-', '-', '-']


]

# [
# ['-', '-', '-'],
# ['-', 'X', 'O'],
# ['X', '-', '-']
# ]
)
M.turn = 'X'
# TM = TreeMat(M, 1)
# TM.setCostAndExpand(0)
# print("---------")
# print(TM.cost)
# for child in TM.children:
#     print(child.matrix.buffer)
#     print(child.cost)
#     print(child.lastMove)
#     print("\n")
print(M.calculate())
# print(TM.children[0].matrix.buffer)