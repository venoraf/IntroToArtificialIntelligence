# bonus fr
# To design a safe ship layout, we need to consider the following factors:
# 1. The layout should allow easy access to all open cells so that bots can quickly reach any location.
# 2. It should have a clear path to the fire suppression button.
# 3. The layout should minimize the spread of fire and allow for efficient fire containment.
#start with a 3x3 square with the button in the middle square - since the bot has the first move, button can be reached in one move and no matter where the fire is, it will be extinguished
#then, we incrementally add a square to any open cell and discover which is the best location to add the next cell - to discover we must check all possible combos and return the best option
#keep doing this process until you get to a point where the fire has a higher chance of killing the bot than the bot reaching the button (chances of the bot reaching the button gets very low)

from IPython.core.magic import on_off
from pickle import TRUE
from enum import Enum
import random
import numpy as np
import math

class DoorState(Enum):
    CLOSED = 0
    OPEN = 1

class Cell:

    def __init__(self, x, y):
        self.xCor = x
        self.yCor = y
        self.status = DoorState.CLOSED
        self.onfire = False
        self.fireProbability = 0.0

    def __str__(self):
        return f'X:{self.xCor} Y:{self.yCor} status:{self.status}\n'

    def __repr__(self):
        return f'X:{self.xCor} Y:{self.yCor} status:{self.status}\n'

    def printState(self, botLocation, buttonLocation):
      if botLocation is not None and botLocation.xCor == self.xCor and botLocation.yCor == self.yCor:
        print ('■', end= '')
      elif buttonLocation is not None and buttonLocation.xCor == self.xCor and buttonLocation.yCor == self.yCor:
        print ('@', end= '')
      elif self.onfire:
        print('‡', end = '')
      else:
        if self.status == DoorState.CLOSED:
          print ('∅', end='')
        else:
          print ('O', end='')

OptimalLayout = [[Cell(i, j) for i in range(3)] for j in range(3)]
button_location = OptimalLayout[1][1]
currSize = 3

def addNewCell():
   currSize = currSize + 2
   # it is + 2 because making the cell count even takes away the possibility of having a middle cell and you need to have a middle cell
   OptimalLayout = [[Cell(i, j) for i in range(currSize)] for j in range(currSize)]
   button_location = OptimalLayout[math.floor(currSize/2)][math.floor(currSize/2)]
   # makes sure that the button is in the middle cell making it equally accessible from everywhere

def evaluateLayoutSafety():
  Q = 0.99
  # q is calculated as bot performance between 0 and 1
  # just gotta run tests at this point - whatever logic was done to eval bot 4 needs to be here
  return Q

def allPossibleCombinations():
  overallSafety = 0.0
  safety = 0.0
  for i in range(currSize):
    for j in range(currSize):
      if i == buttonLocation.xCor and j == buttonLocation.yCor:
        continue
      else:
        botLocation = OptimalLayout[i][j]
      for x in range(currSize):
        for y in range(currSize):
          OptimalLayout[x][y].onfire = False
      # this theoretically should be resetting all the prev fires that were lit
      for x in range(currSize):
        for y in range(currSize):
          if x == buttonLocation.xCor and y == buttonLocation.yCor:
            continue
          if x == botLocation.xCor and y == botLocation.yCor:
            continue
          OptimalLayout[x][y].onfire = True
          safety = safety + evaluateLayoutSafety
  safety = safety/((currSize*currSize) - 2)
  # safety is normalized for total fire Locations
  # the - 2 is for the bot and button cells that the fire can't use/slay
  safety = safety/((currSize*currSize) - 1)
  # safety is normalized for total bot Locations
  # the - 1 is for the button that the bot can't be in/slay
  return safety
  safeDesign = True
  overallSafety = 1.0
  while safeDesign:
    addNewCell()
    currSafety = allPossibleCombinations()
    if currSafety < .6:
      #safety under .6 is considered an unsafe layout
      currSize = currSize - 1
      #layout is not safe so we return to the prev layout
      OptimalLayout = [[Cell(i, j) for i in range(3)] for j in range(3)]
      break

print('OptimalLayout[',currSize,'][',currSize,']')
