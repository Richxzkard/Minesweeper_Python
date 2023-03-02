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
import time
from queue import Queue
import random


class MyAI( AI ):



	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################



		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.minesLeft = totalMines
		self.covered = rowDimension * colDimension
		self.safeQueue = Queue()

		self.willbeUncovered = 0
		self.board = []
		self.startX = startX
		self.startY = startY
		self.frontier = {}
		self.safe = {}
		self.uncovered = {}
		self.guess = {}
		self.totalUncovered = 0

		self.initiateBoard()

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		if self.covered <= self.totalMines:
			return Action(AI.Action.LEAVE)


		self.willbeUncovered = 0

		self.totalUncovered += 1
		self.board[self.startY][self.startX][0] = number
		self.board[self.startY][self.startX][1] = number - self._numMarkedNeighbors(self.startX, self.startY)
		self._updateNeighbors(self.startX, self.startY, number)

		if self.willbeUncovered == 1:
			self.board[self.startY][self.startX][0] = number
		else:
			self.board[self.startY][self.startX][1] = number - self._numMarkedNeighbors(self.startX, self.startY)



		if self.getEffectiveLabel(self.startX, self.startY) == self.getNumUnmarkedNeighbors(self.startX, self.startY):
			self.FlagAdjacent(self.startX, self.startY)

		

		if self.frontier and self.uncovered and not self.safe:
			check = self.modelCheck()

			for tile in check[0]:
				if tile not in self.safe:
					self.safe[tile] = self.board[tile[1]][tile[0]]

			for tile in check[1]:
				flag_x, flag_y = tile[0], tile[1]
				self.board[flag_y][flag_x][0] = 'M'
				self.board[flag_y][flag_x][1] = None
				self.minesLeft -= 1
				self._updateFlagNeighbors(flag_x, flag_y)
				if tile in self.frontier:
					self.frontier.pop(tile)
			if len(check[2]) != 0:
				for tile in check[2]:
					self.guess[tile] = self.board[tile[1]][tile[0]]




		#
		# if self.safe:
		# 	x, y = self.safe.popitem()[0]
		# elif self.frontier:
		# 	x, y = self.frontier.popitem()[0]
		# 	while (self.frontier):
		# 		if self.getLabel(x, y) == '*':
		# 			break
		# 		else:
		# 			x, y = self.frontier.popitem()[0]
		# else:
		# 	if self.guess:
		# 		x, y = self.guess.popitem()[0]
		# 	else:
		# 		x = random.randrange(self.colDimension)
		# 		y = random.randrange(self.rowDimension)
		#
		# 	self.guess.clear()
		# 	self.covered -= 1
		#
		# 	self.startX = x
		# 	self.startY = y
		#
		# 	return Action(AI.Action.UNCOVER, x, y)

		action = AI.Action(1)
		if self.safe:
			x, y = self.safe.popitem()[0]
		elif self.frontier:
			x, y = self.frontier.popitem()[0]
			while (self.frontier):
				if self.getLabel(x, y) == '*':
					break
				else:
					x, y = self.frontier.popitem()[0]
		else:
			if self.guess:
				x, y = self.guess.popitem()[0]
			else:
				x = random.randrange(self.colDimension)
				y = random.randrange(self.rowDimension)

		# print("x, y: ", x, y)
		self.guess.clear()
		self.covered -= 1

		self.startX = x
		self.startY = y

		return Action(action, x, y)


def getLabel(self, x, y):
		return self.board[y][x][0]

	def getEffectiveLabel(self, x, y):
		return self.board[y][x][1]

	def getNumUnmarkedNeighbors(self, x: int, y: int) -> int:
		return self.board[y][x][2]

	def _checkRule(self, x: int, y: int) -> None:
		if self.getEffectiveLabel(x, y) == self.getNumUnmarkedNeighbors(x, y):
			self.FlagAdjacent(x, y)

	def FlagAdjacent(self, col: int, row: int) -> None:
		for x in [col-1, col, col+1]:
			for y in [row-1, row, row+1]:
				if (x >= 0 and y>= 0) and (x < self.colDimension and
					y < self.rowDimension) and (x != col or y != row) and\
					(self.getLabel(x, y) == '*'):
					self.board[y][x][0] = 'M'
					self.board[y][x][1] = None
					self._updateFlagNeighbors(x, y)
					self.minesLeft -= 1

	def _updateFlagNeighbors(self, col: int, row: int) -> None:
		for x in [col-1, col, col+1]:
			for y in [row-1, row, row+1]:
				if (x >= 0 and y>= 0) and (x < self.colDimension and
					y < self.rowDimension) and (x != col or y != row) and (
					self.getLabel(x, y) != 'M'):
					if self.getLabel(x, y) != '*':
						self._updateEffectiveLabel(x, y)
					self._updateAdjacentTileNum(x, y)


	def _updateNeighbors(self, col: int, row: int, number: int) -> None:
		if number == 0 or self.getEffectiveLabel(col, row) == 0:
			self._effectiveZero(col, row, True)
		else:
			for x in [col-1, col, col+1]: 
				for y in [row-1, row, row+1]:
					if (x >= 0 and y >= 0) and (x < self.colDimension and
						y < self.rowDimension) and (x != col or y != row):
						self._updateAdjacentTileNum(x, y)

						if (x, y) not in self.safe:
							if ((x, y) not in self.frontier and
								self.getLabel(x, y) == '*'):
								self.frontier.update({(x,y):self.board[y][x]})
			self.uncovered.update({(col, row):self.board[row][col]})

	def _effectiveZero(self, col: int, row: int, uncover = False) -> None:
		if uncover:
			for x in [col-1, col, col+1]: 
				for y in [row-1, row, row+1]:
					if (x >= 0 and y >= 0) and (x < self.colDimension and
						y < self.rowDimension) and (x != col or y != row):
						self._updateAdjacentTileNum(x, y)
						if (x, y) not in self.safe and self.getLabel(x, y) == '*':
							self.safe.update({(x, y):self.board[y][x]})
						if (x, y) in self.frontier:
							self.frontier.pop((x, y))
		else:
			for x in [col-1, col, col+1]: 
				for y in [row-1, row, row+1]:
					if (x >= 0 and y >= 0) and (x < self.colDimension and
						y < self.rowDimension) and (x != col or y != row):
						# add (x, y) to safe dict
						if (x, y) not in self.safe and self.getLabel(x, y) == '*':
							self.safe.update({(x, y):self.board[y][x]})
						# remove (x, y) from frontier dict
						if (x, y) in self.frontier:
							self.frontier.pop((x, y))


	
	def _updateAdjacentTileNum(self, x:int, y:int) -> None:
		self.board[y][x][2] -= 1
		if self.board[y][x][2] == 0 and (x, y) in self.uncovered:
			self.uncovered.pop((x, y))
		self._checkRule(x, y)

	def _updateEffectiveLabel(self, x: int, y:int) -> None:
		if self.board[y][x][1]:
			self.board[y][x][1] -= 1
		self._checkRule(x, y)
		if self.getEffectiveLabel(x, y) == 0: 
			self._effectiveZero(x, y, False)
			

	def unmarkedNeighbors(self, colX: int, rowY:int) -> list:
		neighbors = list()
		for x in [colX-1, colX, colX+1]: 
			for y in [rowY-1, rowY, rowY+1]:
				if (x >= 0 and y >= 0) and (x < self.colDimension and
				y < self.rowDimension) and (x != colX or y != rowY):
					if (self.board[y][x][0] == '*'):
						neighbors.append((x, y))

		return neighbors
	
	def _updateBoard(self, x: int, y: int, number: int) -> None:
		self.board[y][x][0] = number
		self.board[y][x][1] = number - self._numMarkedNeighbors(x, y)
		self._updateNeighbors(x, y, number)


	def _numMarkedNeighbors(self, col: int, row: int) -> int:
		count = 0
		for x in [col-1, col, col+1]: 
			for y in [row-1, row, row+1]:
				if (x >= 0 and y >= 0) and (x < self.colDimension and
				y < self.rowDimension) and (x != col or y != row):
					if self.board[y][x][0] == 'M':
						count += 1
		return count


	def getUncoveredNeighbors(self, colX: int, rowY:int) -> list:
		neighbors = list()
		for x in [colX-1, colX, colX+1]: 
			for y in [rowY-1, rowY, rowY+1]:
				if (x >= 0 and y >= 0) and (x < self.colDimension and
				y < self.rowDimension) and (x != colX or y != rowY):
					if (self.board[y][x][0] != '*' and self.board[y][x][0] != 'M'):
						neighbors.append((x, y))
		return neighbors

	def modelCheck(self) -> dict:
		variables = list()
		frontier_uncovered = dict()
		
		variables = self.getCoveredFrontiers()
		start = self.frontier.popitem()
		self.frontier.update({start[0]:start[1]})
		starting_tile = start[0]
		
		for tile in variables:
			uncovered = self.getUncoveredNeighbors(tile[0], tile[1])
			for neighbor in uncovered:
				if neighbor not in frontier_uncovered:
					frontier_uncovered[neighbor] = list()

		for tile in frontier_uncovered:
			covered = self.unmarkedNeighbors(tile[0], tile[1])
			for c in covered:
				if c not in variables:
					variables.append(c)
			frontier_uncovered[tile] = self.unmarkedNeighbors(tile[0], tile[1])
			
		assignment = dict()
		var_num = len(variables)
		solution_dict = dict()
		models = self.getSolutions(assignment, frontier_uncovered, variables, var_num)
		num_of_solutions = len(models)

		for v in variables:
			solution_dict[v] = 0

		solutions = dict()
		solutions[0] = list()
		solutions[1] = list()
		solutions[2] = list()

		for solution in models:
			for tile in solution_dict:
				if solution[tile] == 1:
					solution_dict[tile] += 1
	
		for tile in solution_dict:
			if (solution_dict[tile]/num_of_solutions) == 1:
				solutions[1].append(tile)
			elif (solution_dict[tile]/num_of_solutions) == 0:
				solutions[0].append(tile)

		if len(solutions[0]) == 0 and len(solutions[1]) == 0 and models is not None:

			guessTile = min(solution_dict, key = lambda x: x[1])
			solutions[2].append(guessTile)
					
		return solutions

	def satisfyConstraint(self, variables, constraint):

		for c in constraint:
			sum = 0 
			num = len(constraint[c])
			i = 0
			x, y = c
			label = self.getEffectiveLabel(x, y)
			for var in constraint[c]:
				if var in variables:
					sum += variables[var]
					i += 1
			if i == num and sum != label:
				return False
			elif i < num and sum > label:
				return False
		return True
	
	def getSolutions(self, assign, constraints, vars, num):

		solutions = []
		if num == 0:
			return [assign]
		for v in vars:
			if v in assign: 
				continue
			assign[v] = 0
			if self.satisfyConstraint(assign, constraints): 
				assign_copy = assign.copy()
				solutions += self.getSolutions(assign_copy, constraints, vars, num-1) 
			assign[v] = 1
			if self.satisfyConstraint(assign, constraints):
				assign_copy = assign.copy()
				solutions += self.getSolutions(assign_copy, constraints, vars, num-1)

			return solutions		

	def getCoveredFrontiers(self) -> list:

		final_frontier = list()
		if len(self.frontier) < 25:
			return self.frontier

		frontier_copy = self.frontier.copy()
		for tile in self.frontier:
			if tile not in frontier_copy:
				continue
			starting_tile = tile
			frontier_copy.pop(tile)
			current_frontier = list()
			current_frontier.append(starting_tile)
			f = list()
			f.append(starting_tile)
			while f:
				tile = f.pop() 
				neighbors = self.unmarkedNeighbors(tile[0], tile[1])
				for n in neighbors:
					if n in frontier_copy and n not in current_frontier:
						current_frontier.append(n)
						f.append(n)
			if len(current_frontier) < 25:
				final_frontier.append(current_frontier)

		return max(final_frontier, key = lambda x: len(x))



	def initiateBoard(self):
		for i in range(self.rowDimension):
			row = []
			for j in range(self.colDimension):
				if (i == 0 or i == self.rowDimension - 1) and (j == 0 or j == self.colDimension -1):
					row.append(['*', None, 3])
				elif i == 0 or i == self.rowDimension - 1 or j == 0 or j == self.colDimension -1:
					row.append(['*', None, 5])
				else:
					row.append(['*', None, 8])
			self.board.append(row)
		self.covered -= 1



		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################