# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class Tile():
        def __init__(self):
                self.label = -1# 0: empty, 1-8: adjacent mines (getAction "number"), -1: covered, -2 = flag 
                self.e_label = -1 # effective label: label - neighbouring flags
                self.p_mine = -1 # probability of mine
                #self.
        def __repr__(self):
                return f'{self.label}'

class MyAI( AI ):

        def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
                self.board = []
                self.tiles = dict() 
               # self.board.append([i for i in range(0,colDimension+1)])
                for i in range(rowDimension):
                        self.board.append([])
                      #  self.board[i].append(rowDimension-i+1)
                        for j in range(colDimension):
##                                if i == 0:
##                                        self.board[i].append(j)
##                                        continue
##                                if j == 0:
##                                        self.board[i].append(rowDimension-i+1)
##                                        continue
                                self.tiles[(j,i)] = -1
                                self.board[i].append(Tile())
                
                self.mines = totalMines
                self.rows = rowDimension
                self.cols = colDimension
                self.time = 360
                self.moves = 0
                self.flags = 0
                self.uncoveredTiles = 0
                self.requiredUncovers = (rowDimension*colDimension) - totalMines
                self.startX = startX
                self.startY = startY
                self.lastAction = None
                self.frontier = set()
                self.neighbours = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
                self.ones = set()

        def uncoverTile(self,x,y):
                self.moves += 1
                self.uncoveredTiles += 1
                action = AI.Action.UNCOVER
                self.lastAction = action
                self.lastX = x
                self.lastY = y
                del self.tiles[(x,y)]
                        
                        
        def getAction(self, number: int) -> "Action Object":
                if self.moves == 0:
                        #print('start:',self.startX+1,self.startY+1)
                        self.uncoverTile(self.startX,self.startY)
                        #return Action(AI.Action.UNCOVER, self.startX, self.startY)
                
                if self.uncoveredTiles == self.requiredUncovers:
                        return Action(AI.Action.LEAVE)
                
                                
                if self.lastAction == AI.Action.UNCOVER:
                        self.board[self.rows-self.lastY-1][self.lastX].label = number
                        
                        
##                        if len(self.frontier) > 0:
##                                nextc = self.frontier.pop()
##                                self.uncoverTile(nextc[0],nextc[1])
##                                return Action(AI.Action.UNCOVER, nextc[0],nextc[1])
##                                
##                        coord = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
##                        for i,j in coord:
##                                if self.valid_row(self.lastY+j) and self.valid_col(self.lastX+i):
##                                        self.frontier.add((self.lastX+i,self.lastY+j))
##                        nextc = self.frontier.pop()
##                        self.uncoverTile(nextc[0],nextc[1])
##                        return Action(AI.Action.UNCOVER, nextc[0],nextc[1])
##                        
####                        if number == 0:
##                        if len(self.frontier) > 0:
##                                nextc = self.frontier.pop()
##                                self.uncoverTile(nextc[0],nextc[1])
##                                return Action(AI.Action.UNCOVER, nextc[0],nextc[1])
                      #  print(self.lastX,self.lastY)

                        if number == 0:
                                for i,j in self.neighbours:
                                        newX = self.lastX+i
                                        newY = self.lastY+j
                                        if self.valid_row(newY) and self.valid_col(newX) and self.board[self.rows-newY-1][newX].label == -1:
                                                self.frontier.add((newX,newY))
                        if number >= 1:
                                self.ones.add((self.lastX,self.lastY))
                        
                        if len(self.frontier) > 0:
##                                print(self.frontier)
                                nextc = self.frontier.pop()
                                self.uncoverTile(nextc[0],nextc[1])
                             #   print('Next:',nextc[0]+1,nextc[1]+1)
                                return Action(AI.Action.UNCOVER, nextc[0],nextc[1])
                        
                        

                        if self.rows == 5 and self.cols == 5 and self.flags < 1:
                                for x,y in self.ones:
                                        neighbour = self.one_uncovered_neighbour(x,y)
                                        if  neighbour != None:
                                                self.board[self.rows-neighbour[1]-1][neighbour[0]].label = -2 #flag
                                                del self.tiles[(neighbour[0],neighbour[1])]
                                                self.flags += 1
                                                return Action(AI.Action.FLAG, neighbour[0],neighbour[1])

                      #  print("tiles:" ,self.tiles)        
                        for i,j in self.tiles.keys():
                                self.uncoverTile(i,j)
                                return Action(AI.Action.UNCOVER, i,j)            
                return Action(AI.Action.LEAVE)

        def one_uncovered_neighbour(self,x,y):
                neighbour = []
                for i,j in self.neighbours:
                        newX = x+i
                        newY = y+j
                        #print(self.board[self.rows-newY-1][newX].label,end=" ")
                        if self.valid_row(newY) and self.valid_col(newX) and self.board[self.rows-newY-1][newX].label == -1:
                                neighbour.append((newX,newY))
                if len(neighbour) == 1:
                        return neighbour[0]
                else:
                        return None

        def valid_row(self,row):
                return row in range(self.rows)

        def valid_col(self,col):
                return col in range(self.cols)

        def print_board(self):
                for i in range(self.rows):
                        print(f'{self.rows-i} | '.center(5),end='')
                        for j in range(self.cols):
                                x = str(self.board[i][j]).rjust(2)
                                print(x,end=' ')
                        print()
                print('----'*self.cols)
                print(f'0 | '.center(5),end='')
                for i in range(1,len(self.board[0])+1):
                        m = str(i).rjust(2)
                        print(m,end=' ')
                print('\n')
                
                        
if __name__ == '__main__':
        x = MyAI(5,5,1,4,4)
##        x.print_board()
##        print_board(x.board)
        x.getAction(0)
        x.print_board()
##        x.getAction(0)
####        print_board(x.board)
##        x.getAction(0)
####        print_board(x.board)
##        x.getAction(0)
####        print_board(x.board)
##        x.getAction(0)
##        x.getAction(0)
##        x.getAction(0)
##        x.getAction(0)
##        x.getAction(0)
##        x.getAction(0)
        for _ in range(26):
                x.getAction(0)
                
        x.print_board()
##        print(x.frontier)
