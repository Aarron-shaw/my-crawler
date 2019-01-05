#!/usr/bin/env python3

"""
Code based on array_grid.py found @

 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""


import pygame
import random






pygame.init()
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PASTLE_BLUE = (6, 103, 132)
GREY = (128,128,128)
PINK = (255,105,180)

slower = False
RNG = 0.15
# GRID DEFS
# 0 = empty
# 1 = player
# 2 = ai
# 3 = animation
# 4 = item
# 5 = door

#DEBUGGING SETTING #0 is off, 1 is low, 2 is high
DEBUG = 2

# Set the HEIGHT and WIDTH of the screen

WINDOW_SIZE = [500,700]
if DEBUG > 1 and DEBUG < 2: print(WINDOW_SIZE)
#This sets the max borders for the moving pieces
LIMIT_DR = WINDOW_SIZE[0] #down right
LIMIT_UL = 0 #up left




# This sets the margin between each cell
MARGIN = 0
MATRIX = 25

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = WINDOW_SIZE[0] // (MATRIX + MARGIN)
HEIGHT = WINDOW_SIZE[0] // (MATRIX + MARGIN)
#FPS
FPS = 10
# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(MATRIX):
	# Add an empty array that will hold each cell
	# in this row
	grid.append([])
	for column in range(MATRIX):
		grid[row].append(0)  # Append a cell
		
#Global variables for objects 

enemy_list = ["Goblin","Rats","Giant rat","Snail","zombie","Vampire","Ghost","witch","Org","Orc","Special"]

object_list = ["gold","silver","trash","wood","iron","leather","cloth","potion","meal","water","special"]

#Set a bunch of default values

timer = 0
direction = "left"
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Basic functions to help keep code clean

def myround(x, base=WIDTH):
	return int(base * round(float(x)/base))

def xy2grid(x,y):
	row = x // ((WIDTH + MARGIN))
	col = y // ((WIDTH + MARGIN))
	return row,col

def x2grid(x):
	row = x // ((WIDTH + MARGIN))
	return row
	
	#return true if block is 0 or the block is the same as our choice. 
def chk_blk_ocpy(block_type,x,y):
	row = x2grid(x) 
	col = x2grid(y)
	if row > MATRIX-1: return False
	if col > MATRIX-1: return False
	if not grid[row][col] == 0 or grid[row][col] == block_type:
		return True
	else:
		return False
		
def chk_blk_border(x,y):
	if x > LIMIT_DR:
		return False
	if y > LIMIT_DR:
		return False
	if x < LIMIT_UL:
		return False
	if y < LIMIT_UL:
		return False
	else:
		return True
		
def chk_side(x,y):
	row = x2grid(x)
	col = x2grid(y)
	if row <= 1 and col <= MATRIX:
		return 1
	if row >= 2 and col >= MATRIX-1:
		return 2
	if row >= MATRIX-1 and col >= 0:
		return 3
	if row <= MATRIX and col <= 1:
		return 4

def chk_row(q,x,y):
	row = x2grid(x)
	col = x2grid(y)
	if q == 1:
		return col
	if q == 2: 
		return row
	if q == 3: 
		return col
	if q == 4:
		return row

def chk_limit(x,y):
	if x >= LIMIT_DR:
		x = LIMIT_DR-WIDTH+MARGIN
	if x < LIMIT_UL:
		x = LIMIT_UL
	if y >= LIMIT_DR:
		y = LIMIT_DR-WIDTH+MARGIN
	if y < LIMIT_UL:
		y = LIMIT_UL
	return x,y

		
#Classes

class Item(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.name = object_list[random.randint(0,10)]
		self.amount = random.randint(1,4)
		
		
	
	
		

class ObjHuman(object):
	def __init__(self,x,y,l_x,l_y,direction):
		self.x = x
		self.y = y
		#last x,y
		self.l_x = l_x
		self.l_y = l_y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		#last row/col
		self.l_row = self.l_x // ((WIDTH + MARGIN))
		self.l_col = self.l_y // ((WIDTH + MARGIN))
		self.direction = direction
		
		
		#Player stats
		self.hp = 100
		self.gold = 0
		self.silver = 0
		self.trash = 0
		self.wood = 0
		self.iron = 0
		self.leather = 0
		self.cloth = 0
		self.potion = 0
		self.meal = 0
		self.water = 0
		self.special = 0
		
		#projectiles
		self.p_x = x
		self.p_y = y
		self.p_row = self.row
		self.p_col = self.col
		self.p_direction = direction
		
	def debug_self(self):
		# print("x:{},y:{},p_x:{},p_y:{}".format(self.x,self.y,self.p_x,self.p_y))
		# print("p_row:{},p_col:{}".format(self.p_row,self.p_col))
		#print(self.p_x,self.p_y)
		pass
	def move(self,direction,x,y):

		q = 1
		#up,down,left,right are all repeated cases. 
		#as each case is slightly different. 
		if direction == "up":
			#if our height is greater than the limit we can move
			#defailt is 0
			if self.x > LIMIT_UL:
				self.x -= (WIDTH + MARGIN)
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				#== 2 is AI occupied return to our position
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: 
						print("CONFLICT",grid[self.row][self.col])
					#if the target grid is a door, we clean the map and 
					#generate a new one and switch sides of our player
					#based on our original side. 
					
					if grid[self.row][self.col] == 5:
						q = chk_side(self.x,self.y)
						clean_map()
						sq = chk_row(q,self.x,self.y)
						gen_map(q,sq)
						if q == 1:
							self.x = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 2:
							self.y = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)		
						if q == 3:
							self.x = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 4:
							self.y = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
					#We can't occupy the grid, move back. 
					else:
						self.x += (WIDTH + MARGIN)
						self.col = self.y // (WIDTH + MARGIN)
						self.row = self.x // (HEIGHT + MARGIN)
				#0 is free, so we can occupy it.
				if grid[self.row][self.col] == 0:
					grid[self.row][self.col] = 1
					grid[self.l_row][self.l_col] = 0
					self.l_row = self.row
					self.l_col = self.col
			# if we managed to go below the border, reset the position.
			if self.x < LIMIT_UL:
				self.x = LIMIT_UL
			self.direction = "up"
			##print(self.x,self.y,self.row,self.col)

		if direction == "down":

			if self.x < (LIMIT_DR - HEIGHT):
				self.x += (WIDTH + MARGIN)
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: print("CONFLICT")
					if grid[self.row][self.col] == 5:
						q = chk_side(self.x,self.y)
						clean_map()
						sq = chk_row(q,self.x,self.y)
						gen_map(q,sq)
						if q == 1:
							self.x = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 2:
							self.y = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)		
						if q == 3:
							self.x = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 4:
							self.y = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)						
					else:
						self.x -= (WIDTH + MARGIN)
						self.col = self.y // (WIDTH + MARGIN)
						self.row = self.x // (HEIGHT + MARGIN)
				if grid[self.row][self.col] == 0:
					grid[self.row][self.col] = 1
					grid[self.l_row][self.l_col] = 0
					self.l_row = self.row
					self.l_col = self.col
			if self.y > LIMIT_DR:
				self.y = LIMIT_DR
			self.direction = "down"
			##print(self.x,self.y,self.row,self.col)

		if direction == "left":
			if self.y > LIMIT_UL:
				self.y -= (WIDTH + MARGIN)
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: print("CONFLICT")
					if grid[self.row][self.col] == 5:
						q = chk_side(self.x,self.y)
						clean_map()
						sq = chk_row(q,self.x,self.y)
						gen_map(q,sq)
						if q == 1:
							self.x = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 2:
							self.y = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)		
						if q == 3:
							self.x = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 4:
							self.y = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
					else:
						self.y += (WIDTH + MARGIN)
						self.col = self.y // (WIDTH + MARGIN)
						self.row = self.x // (HEIGHT + MARGIN)
				if grid[self.row][self.col] == 0:
					grid[self.row][self.col] = 1
					grid[self.l_row][self.l_col] = 0
					self.l_row = self.row
					self.l_col = self.col
			if self.y > LIMIT_DR:
				self.y = LIMIT_DR
			##print(self.x,self.y,self.row,self.col)
			self.direction = "left"


		if direction == "right":

			if self.y < (LIMIT_DR - WIDTH):
				self.y += (WIDTH + MARGIN)
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: print("CONFLICT")
					if grid[self.row][self.col] == 5:
						q = chk_side(self.x,self.y)
						clean_map()
						sq = chk_row(q,self.x,self.y)
						gen_map(q,sq)
						if q == 1:
							self.x = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 2:
							self.y = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)		
						if q == 3:
							self.x = LIMIT_UL + WIDTH
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
						if q == 4:
							self.y = LIMIT_DR - (WIDTH * 2)
							self.col = self.y // (WIDTH + MARGIN)
							self.row = self.x // (HEIGHT + MARGIN)
							##print(self.x,self.y,self.row,self.col)
					else:
						self.y -= (WIDTH + MARGIN)
						self.col = self.y // (WIDTH + MARGIN)
						self.row = self.x // (HEIGHT + MARGIN)
				if grid[self.row][self.col] == 0:
					grid[self.row][self.col] = 1
					grid[self.l_row][self.l_col] = 0
					self.l_row = self.row
					self.l_col = self.col
			if self.y > LIMIT_DR:
				self.y = LIMIT_DR
			##print(self.x,self.y,self.row,self.col)
			self.direction = "right"

	def check_collision(self,x,y,direction):

	#check for collision boarder.
		self.direction = direction
		self.p_x = x 
		self.p_y = y
		self.p_row = self.p_x // ((WIDTH + MARGIN))
		self.p_col = self.p_y // ((WIDTH + MARGIN))
		
		if direction == "up":
			if not (x-WIDTH) <= LIMIT_UL:
				self.p_x = (x-WIDTH)
				self.p_row = self.p_x // ((WIDTH + MARGIN))
				#print(self.p_x,self.p_y,self.p_row,self.p_col,self.p_direction)
				grid[self.p_row][self.p_col] = 3
				
		if direction == "down":
			if not (x+WIDTH) >= LIMIT_DR:
				self.p_x = (x+WIDTH+MARGIN)
				self.p_row = self.p_x // ((WIDTH + MARGIN))
				#print(self.p_x,self.p_y,self.p_row,self.p_col,self.p_direction,LIMIT_DR)
				grid[self.p_row][self.p_col] = 3
				
		if direction == "left":
			if not (y-WIDTH) < LIMIT_UL:
				self.p_y = (y-WIDTH)
				self.p_col = self.p_y // ((WIDTH + MARGIN))
				#print(self.p_x,self.p_y,self.p_row,self.p_col,self.direction)
				grid[self.p_row][self.p_col] = 3
				
		if direction == "right":
			if not (y+WIDTH) > LIMIT_DR:
				self.p_y = (y+WIDTH+MARGIN)
				self.p_col = self.p_y // ((WIDTH + MARGIN))
				#print(self.p_x,self.p_y,self.p_row,self.p_col,self.direction)
				grid[self.p_row][self.p_col] = 3
		if DEBUG == 3: self.debug_self()
		self.debug_self()
		
		for n,i in enumerate(item):
			#print(i.__dict__)
			
			if i.row == self.p_row and i.col == self.p_col:

				if i.name == "gold":
					self.gold += i.amount
				if i.name == "silver":
					self.silver += i.amount	
				if i.name == "trash":
					self.trash += i.amount
				if i.name == "wood":
					self.wood += i.amount
				if i.name == "iron":
					self.iron += i.amount
				if i.name == "leather":
					self.leather += i.amount
				if i.name == "cloth":
					self.cloth += i.amount
				if i.name == "potion":
					self.potion += i.amount
				if i.name == "meal":
					self.meal += i.amount
				if i.name == "water":
					self.water += i.amount
				if i.name == "special":
					self.special += i.amount
				del item[n]
		return FPS * 0.3


class ObjPos(object):
	def __init__(self,x,y,l_x,l_y):
		self.x = x
		self.y = y
		self.l_x = l_x
		self.l_y = l_y
		self.b_x = 0
		self.b_y = 0
		self.direction = 0
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.l_row = self.l_x // ((WIDTH + MARGIN))
		self.l_col = self.l_y // ((WIDTH + MARGIN))
		self.type = enemy_list[random.randint(0,8)]
		self.id = 1
		self.hp = 100
		self.level = 1
		self.attack = random.randint(1,10)
		self.defense = random.randint(1,10)
		

	def update_ai(self,new_x,new_y):
		self.l_x = self.x
		self.l_y = self.y
		self.x = new_x
		self.y = new_y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.l_row = self.l_x // ((WIDTH + MARGIN))
		self.l_col = self.l_y // ((WIDTH + MARGIN))
		
	def find_player_ai(self,h_x,h_y):
		#given the players cords, move on step closer. 
		t_x = self.x - h_x 
		t_y = self.y - h_y
		failstate = 0
		mv_x = 0
		mv_y = 0
		#print(t_x,t_y)
		if self.l_x == self.b_x and self.l_y == self.b_y:
			print("switching?")
			seed = random.randint(0,4)
			
			if seed == 0:
				mv_x -= (WIDTH + MARGIN)

			elif seed == 1:
				mv_y -= (WIDTH + MARGIN)
			elif seed == 2:
				mv_x = 0
				mv_y = 0
				self.b_x = self.x
				self.b_y = self.y
			elif seed == 3:
				mv_y += (WIDTH + MARGIN)

			elif seed == 4:
				mv_x += (WIDTH + MARGIN)
		
		else:
			
			if t_x > 0 and t_y >= 0 and not self.direction == 3:
				print("up")
				mv_x = -WIDTH+MARGIN
				mv_y = 0
				self.direction = 1
				
				
			elif t_x >= 0 and t_y < 0 and not self.direction == 4:
				print("right")
				mv_x = 0
				mv_y = WIDTH+MARGIN
				self.direction = 2
				
			elif t_x < 0 and t_y <= 0 and not self.direction == 1:
				print("down")
				mv_x = WIDTH+MARGIN
				mv_y = 0
				self.direction = 3
				
			elif t_x <= 0 and t_y > 0 and not self.direction == 2:
				print("left")
				mv_x = 0
				mv_y = -WIDTH+MARGIN
				self.direction = 4
			elif t_x == 0 and t_y == 0:
				mv_x = 0
				mv_y = 0
				self.direction = 0
		#This section checks if the target is at the boarder, 
		#if returns True, it's ok to proceed. 
		if chk_blk_border(self.x+mv_x,self.y+mv_y) == True:
		
			#Check if our target is occupied. 
			#False is occupied 

			while chk_blk_ocpy(2,self.x+mv_x,self.y+mv_y) == True:
				seed = random.randint(0,3)
				if seed == 0: #Try move right
					print("trying to move right")
					mv_x = 0
					mv_y = WIDTH+MARGIN
					if chk_blk_ocpy(2,self.x+mv_x,self.y+mv_y) == False:
						if chk_blk_border(self.x+mv_x,self.y+mv_y) == True:
							break
					else:
						print("failstate")
						failstate += 1
						self.b_x = self.x
						self.b_y = self.y
				elif seed == 1: #try move left
					print("trying to move left")
					mv_x = 0
					mv_y = -WIDTH+MARGIN
					if chk_blk_ocpy(2,self.x+mv_x,self.y+mv_y) == False:
						if chk_blk_border(self.x+mv_x,self.y+mv_y) == True:
							break
					else:
						print("failstate")
						failstate += 1
						self.b_x = self.x
						self.b_y = self.y
						
				elif seed == 2: #ry move down
					print("trying to move down")
					mv_x = -WIDTH+MARGIN
					mv_y = 0
					if chk_blk_ocpy(2,self.x+mv_x,self.y+mv_y) == False:
						if chk_blk_border(self.x+mv_x,self.y+mv_y) == True:
							break
					else:
						print("failstate")
						failstate += 1
						self.b_x = self.x
						self.b_y = self.y						
				elif seed == 3: #try move up
					print("trying to move down")
					mv_x = WIDTH+MARGIN
					mv_y = 0
					if chk_blk_ocpy(2,self.x+mv_x,self.y+mv_y) == False:
						if chk_blk_border(self.x+mv_x,self.y+mv_y) == True:
							break
					else:
						print("failstate")
						failstate += 1
						self.b_x = self.x
						self.b_y = self.y				
					
				
			print(failstate)
			safe_x,safe_y = chk_limit(self.x+mv_x,self.y+mv_y)
			chk = xy2grid(safe_x,safe_y)
			if grid[chk[0]][chk[1]] == 4:
				print("ate item")
			self.update_ai(safe_x,safe_y)
			print(safe_x,safe_y)



	


#Map functions 

#This function sets an int either +2 or -2 to "swap sides of the map"
def entrance_to_exit(int):
	if int <= 2:
		int = int + 2
	else:
		int = int - 2
	return int
	
	#Set all of our none player grids to 0 to clean it and initialise a new AI.
def clean_map():
	global c_ai_pos
	for row in range(MATRIX):
		for column in range(MATRIX):
			if not grid[row][column] == 1:
				grid[row][column] = 0
	del c_ai_pos

	 

def gen_map(entrance,square):
	global item
	global c_ai_pos
	#first step is to generate doors at the edge of the map
	#Creates a set of exits for the room
	exits = [entrance_to_exit(entrance)]
	for i in range(1,random.randint(1,4)):
		random_check = random.randint(1,4)
		if random_check not in exits:
			exits.append(random_check)
	for q in exits:
		if q == 1:
			if q == exits[0]:
				door_one = square
			else:
				door_one = random.randint(0,MATRIX-1)
			
			grid[0][door_one] = 5
		if q == 2:
			if q == exits[0]:
				door_one = square
			else:
				door_one = random.randint(0,MATRIX-1)
			grid[door_one][MATRIX-1] = 5	
		if q == 3:
			if q == exits[0]:
				door_one = square
			else:
				door_one = random.randint(0,MATRIX-1)
			grid[MATRIX-1][door_one] = 5
		if q == 4:
			if q == exits[0]:
				door_one = square
			else:
				door_one = random.randint(0,MATRIX-1)
			grid[door_one][0] = 5
	p = 0
	#Generate items in the map. 
	item = []
	for row in range(MATRIX):
		for column in range(MATRIX):
			x = row * (WIDTH + MARGIN)
			y = column * (WIDTH + MARGIN)
			seed = random.randint(1,(MATRIX * MATRIX))
			if seed < (MATRIX * MATRIX) * RNG:
				print(str(seed), str((MATRIX * MATRIX) * RNG))
				if not grid[row][column] == 0:
					#can't place here as door is here
					try:
						if grid[row-1][column-1] == 0:
							item.append(Item(x,y))
							grid[row-1][column-1] = 4
					except:
						print("Error")
				else:
					grid[row][column] = 4
					item.append(Item(x,y))
					#print(item[p].__dict__)
				p += 1
				
	#Generate the AI
	c_ai_pos = []
	print(str(LIMIT_UL),str(MATRIX * WIDTH))
	for i in range(0,random.randint(1,5)):
		print(i)
		ai_square_x = myround(random.randint(LIMIT_UL,(MATRIX * WIDTH)))
		ai_square_y = myround(random.randint(LIMIT_UL,(MATRIX * WIDTH)))
		c_ai_pos.append(ObjPos(ai_square_x,ai_square_y,ai_square_x,ai_square_y))
						
						
#AI functions
def pick_square_ai(x,y):

	#Pick a new square based on current x,y cords
	#It will either move one square up,down,left,right or stay in the same place
	state = False
	while not state:
		seed = random.randint(0,4)


		if seed == 0:
			x -= (WIDTH + MARGIN)

		if seed == 1:
			y -= (WIDTH + MARGIN)
		if seed == 2:
			x = x
			y = y
		if seed == 3:
			y += (WIDTH + MARGIN)

		if seed == 4:
			x += (WIDTH + MARGIN)

		x = myround(x)
		y = myround(y)
		#Don't allow the cords to be higher/lower than the border edges.
		if x < LIMIT_UL:
			x = LIMIT_UL + WIDTH
			# print("Here 1:")

		if x > (LIMIT_DR - WIDTH):
			x = LIMIT_DR - WIDTH
			# print("Here 2:")
		if y < LIMIT_UL:
			y = LIMIT_UL + WIDTH
			# print("Here 3:")
		if y > (LIMIT_DR - WIDTH):
			y = LIMIT_DR - WIDTH
			# print("Here 4:")
		state = chk_blk_ocpy(0,x,y)
		print(state)

	return x,y

#Initialise our player and ai object. 


# ai_square_x = random.randint(LIMIT_UL,LIMIT_DR)
# ai_square_y = random.randint(LIMIT_UL,LIMIT_DR)
# c_ai_pos = ObjPos(ai_square_x,ai_square_y,ai_square_x,ai_square_y)

c_h_pos = ObjHuman(0,0,0,0,"left")
grid[c_h_pos.row][c_h_pos.col] = 1

gen_map(1,random.randint(0,MATRIX-1))

# -------- Main Program Loop -----------
while not done:
	pressed = pygame.key.get_pressed()
	if pressed[pygame.MOUSEBUTTONUP]:
		None 

	if pressed[pygame.K_UP]:
		c_h_pos.move("up",c_h_pos.x,c_h_pos.y)


	if pressed[pygame.K_DOWN]:
		c_h_pos.move("down",c_h_pos.x,c_h_pos.y)


	if pressed[pygame.K_LEFT]:
		c_h_pos.move("left",c_h_pos.x,c_h_pos.y)

	if pressed[pygame.K_RIGHT]:
		c_h_pos.move("right",c_h_pos.x,c_h_pos.y)
	
	if pressed[pygame.K_p]:
		slower = not slower
	if pressed[pygame.K_ESCAPE]:
		done = True
	

	for event in pygame.event.get():  # User did something
		if event.type == pygame.QUIT:  # If user clicked close
			done = True
		if pressed[pygame.K_ESCAPE]:
			done = True	# Flag that we are done so we exit this loop
		if pressed[pygame.K_SPACE]:
			#proj = ObjProjectile(c_h_pos.x,c_h_pos.y,c_h_pos.direction)
			c_h_pos.check_collision(c_h_pos.x,c_h_pos.y,c_h_pos.direction)
		else:
			pass
	if DEBUG == 3: print(c_ai_pos.__dict__)
	
	for v,t in enumerate(c_ai_pos):
		c_ai_pos[v].find_player_ai(c_h_pos.x,c_h_pos.y)
		print(c_ai_pos[v].row,c_ai_pos[v].col,"last: ",c_ai_pos[v].l_row,c_ai_pos[v].l_col)
	
	# if not c_ai_pos.row == c_ai_pos.l_row and c_ai_pos.col == c_ai_pos.l_col:
		grid[c_ai_pos[v].l_row][c_ai_pos[v].l_col] = 0	
		grid[c_ai_pos[v].row][c_ai_pos[v].col] = 2
	#Set up debug window strings
	
	#Player directions
	font = pygame.font.SysFont("comicsansms", 22)
	string_to_print = c_h_pos.direction + "," + str(c_h_pos.l_row) + ":" + str(c_h_pos.l_col)
	h_text = font.render(string_to_print, True, (255, 255, 255))
	#AI INFO
	#ai_string = "Type " + ": " + c_ai_pos.type + ", HP : " + str(c_ai_pos.row) + " : "+ str(c_ai_pos.col)
	#ai_text = font.render(ai_string, True, (255, 255, 255))



	# Set the screen background
	screen.fill(BLACK)
	#if DEBUG == 2: print(timer)
	# if DEBUG == 3: print(grid)
	# Draw the grid
	for row in range(MATRIX):
		for column in range(MATRIX):
			color = WHITE
			if grid[row][column] == 1:
				color = RED
			if grid[row][column] == 2:
				color = GREEN
			if grid[row][column] == 3:
				if timer%2 == 0:
					color = PASTLE_BLUE
					
				else:
					color = BLACK
					print(timer%2)

				if timer == 0:
					grid[row][column] = 0
			if grid[row][column] == 4:
				color = PINK
			if grid[row][column] == 5:
				color = GREY

				#color = WHITE
			#pygame.time.wait(10)
			pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN, WIDTH,HEIGHT])
	screen.blit(h_text,(0, 510 - h_text.get_height() // 2))
	#screen.blit(ai_text,( 0, 530 - ai_text.get_height() // 2))

	# Limit to FPS var
	clock.tick(FPS)
	if slower == True:
	
		pygame.time.delay(300)


	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
