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
#Load some fonts

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
win = pygame.display.Info()
WINDOW_SIZE = [500,700]
if DEBUG > 1 and DEBUG < 2: print(WINDOW_SIZE)
#This sets the max borders for the moving pieces
LIMIT_DR = WINDOW_SIZE[0] #down right
LIMIT_UL = 0 #up left




# This sets the margin between each cell
MARGIN = 0
MATRIX = 25

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = WINDOW_SIZE[0] // MATRIX
HEIGHT = WINDOW_SIZE[0] // MATRIX
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

object_list = ["Gold","Silver","Trash","wood","Iron","Leather","cloth","Potion","Meal","Water","Special"]

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
	
def chk_blk_ocpy(block_type,x,y):
	row = x2grid(x) 
	col = x2grid(y)
	if not grid[row][col] == 0:
		return True
	else:
		return False
		
#Classes

class Item(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.name = object_list[random.randint(0,10)]
		self.amount = random.randint(1,4)
		
		
	
class ObjProjectile(object):
	def __init__(self,x,y,direction):
		self.x = x
		self.y = y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.direction = direction

	
	def check_collision(self,x,y,direction):
	#check for collision boarder.
		self.direction = direction
		if direction == "up":
			if not (x-WIDTH) <= LIMIT_UL:
				self.x = (x-WIDTH)
				self.row = self.x // ((WIDTH + MARGIN))
				print(self.x,self.y,self.row,self.col,self.direction)
				grid[self.row][self.col] = 3
				return FPS * 0.3
		if direction == "down":
			if not (self.x+WIDTH) >= LIMIT_DR:
				self.x = (x+WIDTH)
				self.row = self.x // ((WIDTH + MARGIN))
				print(self.x,self.y,self.row,self.col,self.direction,LIMIT_DR)
				grid[self.row][self.col] = 3
				return FPS * 0.3
		if direction == "left":
			if not (y-WIDTH) <= LIMIT_UL:
				self.y = (y-WIDTH)
				self.col = self.y // ((WIDTH + MARGIN))
				print(self.x,self.y,self.row,self.col,self.direction)
				grid[self.row][self.col] = 3
				return FPS * 0.3
		if direction == "right":
			if not (y+WIDTH) >= LIMIT_DR:
				self.y = (y+WIDTH)
				self.col = self.y // ((WIDTH + MARGIN))
				print(self.x,self.y,self.row,self.col,self.direction)
				grid[self.row][self.col] = 3
				return FPS * 0.3
		
		

class ObjHuman(object):
	def __init__(self,x,y,l_x,l_y,direction):
		self.x = x
		self.y = y
		self.l_x = l_x
		self.l_y = l_y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.l_row = self.l_x // ((WIDTH + MARGIN))
		self.l_col = self.l_y // ((WIDTH + MARGIN))
		self.direction = direction
		self.hp = 100

	def move(self,direction,x,y):


		if direction == "up":
			#if our height is greater than the limit we can move
			#defailt is 0
			if self.x > LIMIT_UL:
				self.x -= WIDTH
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				#== 2 is AI occupied return to our position
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: 
						print("CONFLICT",grid[self.row][self.col])
					if grid[self.row][self.col] == 5:
						clean_map()
						gen_map(1)
					self.x += WIDTH
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
			print(self.x,self.y,self.row,self.col)

		if direction == "down":

			if self.x < (LIMIT_DR - HEIGHT):
				self.x += WIDTH
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: print("CONFLICT")
					if grid[self.row][self.col] == 5:
						clean_map()
						gen_map(1)					
					self.x -= WIDTH
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
			print(self.x,self.y,self.row,self.col)

		if direction == "left":
			if self.y > LIMIT_UL:
				self.y -= WIDTH
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: print("CONFLICT")
					if grid[self.row][self.col] == 5:
						clean_map()
						gen_map(1)
					self.y += WIDTH
					self.col = self.y // (WIDTH + MARGIN)
					self.row = self.x // (HEIGHT + MARGIN)
				if grid[self.row][self.col] == 0:
					grid[self.row][self.col] = 1
					grid[self.l_row][self.l_col] = 0
					self.l_row = self.row
					self.l_col = self.col
			if self.y > LIMIT_DR:
				self.y = LIMIT_DR
			print(self.x,self.y,self.row,self.col)
			self.direction = "left"


		if direction == "right":

			if self.y < (LIMIT_DR - WIDTH):
				self.y += WIDTH
				self.col = self.y // (WIDTH + MARGIN)
				self.row = self.x // (HEIGHT + MARGIN)
				if not grid[self.row][self.col] == 0:
					if DEBUG > 1 and DEBUG < 3: print("CONFLICT")
					if grid[self.row][self.col] == 5:
						clean_map()
						gen_map(1)
					self.y -= WIDTH
					self.col = self.y // (WIDTH + MARGIN)
					self.row = self.x // (HEIGHT + MARGIN)
				if grid[self.row][self.col] == 0:
					grid[self.row][self.col] = 1
					grid[self.l_row][self.l_col] = 0
					self.l_row = self.row
					self.l_col = self.col
			if self.y > LIMIT_DR:
				self.y = LIMIT_DR
			print(self.x,self.y,self.row,self.col)
			self.direction = "right"


class ObjPos(object):
	def __init__(self,x,y,l_x,l_y):
		self.x = x
		self.y = y
		self.l_x = l_x
		self.l_y = l_y
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


	




def entrance_to_exit(int):
	if int <= 2:
		int = int + 2
	else:
		int = int - 2
	return int
	
	
def clean_map():
	global c_ai_pos
	for row in range(MATRIX):
		for column in range(MATRIX):
			if not grid[row][column] == 1:
				grid[row][column] = 0
	del c_ai_pos
	ai_square_x = random.randint(LIMIT_UL,LIMIT_DR)
	ai_square_y = random.randint(LIMIT_UL,LIMIT_DR)
	c_ai_pos = ObjPos(ai_square_x,ai_square_y,ai_square_x,ai_square_y)
	 

def gen_map(entrance):
	#first step is to generate doors at the edge of the map
	#Creates a set of exits for the room
	exits = [entrance_to_exit(entrance)]
	for i in range(1,random.randint(1,4)):
		random_check = random.randint(1,4)
		if random_check not in exits:
			exits.append(random_check)
	for q in exits:
		if q == 1:
			door_one = random.randint(0,MATRIX-1)
			
			grid[0][door_one] = 5
		if q == 2:
			door_one = random.randint(0,MATRIX-1)
			
			grid[door_one][MATRIX-1] = 5	
		if q == 3:
			door_one = random.randint(0,MATRIX-1)
			
			grid[MATRIX-1][door_one] = 5
		if q == 4:
			door_one = random.randint(0,MATRIX-1)
			
			grid[door_one][0] = 5
	p = 0
	item = []
	for row in range(MATRIX):
		for column in range(MATRIX):
			x = row * (WIDTH - MARGIN)
			y = column * (WIDTH - MARGIN)
			seed = random.randint(1,(MATRIX * MATRIX))
			if seed < (MATRIX * MATRIX) * 0.01:
				print(str(seed), str((MATRIX * MATRIX) * 0.01))
				if not grid[row][column] == 0:
					#can't place here as door is here
					try:
						if grid[row-1][column-1] == 0:
							item[p] = Item(x,y)
							grid[row-1][column-1] = 4
					except:
						print("Error")
				else:
					grid[row][column] = 4
					item.append(Item(x,y))
					
						
						
#AI functions
def pick_square_ai(x,y):

	#Pick a new square based on current x,y cords
	#It will either move one square up,down,left,right or stay in the same place
	seed = random.randint(0,4)
	target_x = c_h_pos.x
	target_y = c_h_pos.y
	
	if seed == 0:
		x -= WIDTH

	if seed == 1:
		y -= WIDTH
	if seed == 2:
		x = x
		y = y
	if seed == 3:
		y += WIDTH

	if seed == 4:
		x += WIDTH

	x = myround(x)
	y = myround(y)
	#Don't allow the cords to be higher/lower than the border edges.
	if x < LIMIT_UL:
		x = LIMIT_UL + WIDTH

	if x > (LIMIT_DR - WIDTH):
		x -= WIDTH

	if y < LIMIT_UL:
		y = LIMIT_UL + WIDTH

	if y > (LIMIT_DR - WIDTH):
		y -= WIDTH


	return x,y

#Initialise our player and ai object. 


ai_square_x = random.randint(LIMIT_UL,LIMIT_DR)
ai_square_y = random.randint(LIMIT_UL,LIMIT_DR)
c_ai_pos = ObjPos(ai_square_x,ai_square_y,ai_square_x,ai_square_y)

c_h_pos = ObjHuman(0,0,0,0,"left")
grid[c_h_pos.row][c_h_pos.col] = 1

gen_map(1)

# -------- Main Program Loop -----------
while not done:
	pressed = pygame.key.get_pressed()


	if pressed[pygame.K_UP]:
		c_h_pos.move("up",c_h_pos.x,c_h_pos.y)


	if pressed[pygame.K_DOWN]:
		c_h_pos.move("down",c_h_pos.x,c_h_pos.y)


	if pressed[pygame.K_LEFT]:
		c_h_pos.move("left",c_h_pos.x,c_h_pos.y)

	if pressed[pygame.K_RIGHT]:
		c_h_pos.move("right",c_h_pos.x,c_h_pos.y)



	for event in pygame.event.get():  # User did something
		if event.type == pygame.QUIT:  # If user clicked close
			done = True
		if pressed[pygame.K_ESCAPE]:
			done = True# Flag that we are done so we exit this loop
		if pressed[pygame.K_SPACE]:
			proj = ObjProjectile(c_h_pos.x,c_h_pos.y,c_h_pos.direction)
			proj.check_collision(proj.x,proj.y,proj.direction)
	if DEBUG == 3: print(c_ai_pos.__dict__)
	
	tmp_ai = pick_square_ai(c_ai_pos.x,c_ai_pos.y)

	if grid[x2grid(tmp_ai[0])][x2grid(tmp_ai[1])] == 0:
		c_ai_pos.update_ai(tmp_ai[0],tmp_ai[1])
		grid[c_ai_pos.row][c_ai_pos.col] = 2
		grid[c_ai_pos.l_row][c_ai_pos.l_col] = 0
	if grid[x2grid(tmp_ai[0])][x2grid(tmp_ai[1])] == 1:
		print("OCCUPIED!")

	#Set up debug window strings
	
	#Player directions
	font = pygame.font.SysFont("comicsansms", 22)
	string_to_print = c_h_pos.direction + "," + str(c_h_pos.l_row) + ":" + str(c_h_pos.l_col)
	h_text = font.render(string_to_print, True, (255, 255, 255))
	#AI INFO
	ai_string = "Type " + ": " + c_ai_pos.type + ", HP : " + str(c_ai_pos.hp)
	ai_text = font.render(ai_string, True, (255, 255, 255))



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
					if DEBUG == 2: print("white")
				else:
					color = BLACK
					print(timer%2)
					if DEBUG == 2: print("black")
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
	screen.blit(ai_text,( 0, 530 - ai_text.get_height() // 2))

	# Limit to FPS var
	clock.tick(FPS)


	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
