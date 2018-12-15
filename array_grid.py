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

# GRID DEFS
# 0 = empty
# 1 = player
# 2 = ai
# 3 = animation

#DEBUGGING SETTING #0 is off, 1 is low, 2 is high
DEBUG = 3

# Set the HEIGHT and WIDTH of the screen
win = pygame.display.Info()
WINDOW_SIZE = [500,500]
if DEBUG > 1 and DEBUG < 2: print(WINDOW_SIZE)
#This sets the max borders for the moving pieces
LIMIT_DR = WINDOW_SIZE[0] #down right
LIMIT_UL = 0 #up left




# This sets the margin between each cell
MARGIN = 0
MATRIX = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = WINDOW_SIZE[0] // MATRIX
HEIGHT = WINDOW_SIZE[1] // MATRIX
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

#Set a bunch of default values
#start position
grid[0][0] = 1
pos = [0,0]
#unused Variable
CHANGE_POS = 1

last_col = 0
last_row = 0
timer = 0
direction = "left"
# Initialize pygame
# pygame.init()

#screen = pygame.display.set_mode(0, 0)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Array Backed Grid")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def myround(x, base=WIDTH):
	return int(base * round(float(x)/base))

def xy2grid(x,y):
	row = x // ((WIDTH + MARGIN))
	col = y // ((WIDTH + MARGIN))
	return row,col

def x2grid(x):
	row = x // ((WIDTH + MARGIN))
	return row

class ai_pos(object):
	def __init__(self,x,y,l_x,l_y):
		self.x = x
		self.y = y
		self.l_x = l_x
		self.l_y = l_y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.l_row = self.l_x // ((WIDTH + MARGIN))
		self.l_col = self.l_y // ((WIDTH + MARGIN))
	
	def update_ai(self,new_x,new_y):
		self.l_x = self.x
		self.l_y = self.y
		self.x = new_x
		self.y = new_y
		self.row = self.x // ((WIDTH + MARGIN))
		self.col = self.y // ((WIDTH + MARGIN))
		self.l_row = self.l_x // ((WIDTH + MARGIN))
		self.l_col = self.l_y // ((WIDTH + MARGIN))		

	
#AI functions
#Pick a new square based on current x,y cords
#It will either move one square up,down,left,right or stay in the same place

def pick_square_ai(x,y):
	seed = random.randint(0,4)
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

#set a random square for our ai in x,y form

ai_square_x = random.randint(LIMIT_UL,LIMIT_DR)
ai_square_y = random.randint(LIMIT_UL,LIMIT_DR)
c_ai_pos = ai_pos(ai_square_x,ai_square_y,ai_square_x,ai_square_y)



#function for moving

def move(direction,x,y):
	global last_row
	global last_col
	global CHANGE_POS
	global grid


	if direction == "up":
		#if our height is greater than the limit we can move
		#defailt is 0
		if pos[1] > LIMIT_UL:
			pos[1] -= WIDTH
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)
			#== 2 is AI occupied return to our position
			if grid[row][column] == 2:
				if DEBUG > 1 and DEBUG < 2: print("CONFLICT",grid[row][column])
				pos[1] += WIDTH
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
			#0 is free, so we can occupy it.
			if grid[row][column] == 0:
				grid[row][column] = 1
				grid[last_row][last_col] = 0
				last_row = row
				last_col = column
		# if we managed to go below the border, reset the position.
		if pos[1] < LIMIT_UL:
			pos[1] = LIMIT_UL


	if direction == "down":

		if pos[1] < (LIMIT_DR - HEIGHT):
			pos[1] += WIDTH
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)
			if grid[row][column] == 2:
				if DEBUG > 1 and DEBUG < 2: print("CONFLICT")
				pos[1] -= WIDTH
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
			if grid[row][column] == 0:
				grid[row][column] = 1
				grid[last_row][last_col] = 0
				last_row = row
				last_col = column
		if pos[1] > LIMIT_DR:
			pos[1] = LIMIT_DR


	if direction == "left":
		if pos[0] > LIMIT_UL:
			pos[0] -= WIDTH
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)
			if grid[row][column] == 2:
				if DEBUG > 1 and DEBUG < 2: print("CONFLICT")
				pos[0] += WIDTH
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
			if grid[row][column] == 0:
				grid[row][column] = 1
				grid[last_row][last_col] = 0
				last_row = row
				last_col = column
		if pos[0] < LIMIT_UL:
			pos[0] = LIMIT_UL


	if direction == "right":

		if pos[0] < (LIMIT_DR - WIDTH):
			pos[0] += WIDTH
			column = pos[0] // (WIDTH + MARGIN)
			row = pos[1] // (HEIGHT + MARGIN)
			if grid[row][column] == 2:
				if DEBUG > 1 and DEBUG < 2: print("CONFLICT")
				pos[0] -= WIDTH
				column = pos[0] // (WIDTH + MARGIN)
				row = pos[1] // (HEIGHT + MARGIN)
			if grid[row][column] == 0:
				grid[row][column] = 1
				grid[last_row][last_col] = 0
				last_row = row
				last_col = column
		if pos[0] > LIMIT_DR:
			pos[0] = LIMIT_DR

	#if DEBUG > 1 and DEBUG < 2: print(row,column)

#function to perform a forward "attack"

def attack(x,y,player,direction):
	global grid
	if DEBUG > 1 and DEBUG < 2: print(x,y,player,direction)
	column = x // (WIDTH + MARGIN)
	row = y // (HEIGHT + MARGIN)
	cords = []
	#1,2,3
	#4,5,6
	#7,8,9
	if direction == "up":
		if row > 0:
			row -= 1
			for i in range(3):
				try:
					if column+(i-1) >= 0:
						grid[row][column+(i-1)] = 3
				except:
					print("Error",row,column)
				if DEBUG > 1 and DEBUG < 2: print(row,i)
		else:
			if DEBUG > 1 and DEBUG < 2: print("Can't attack",x,y,player,direction)
			
			
	if direction == "down":
		if DEBUG > 1 and DEBUG < 2: print("ARGS:",x,y,player,direction)
		if row <= LIMIT_DR:
		
			row += 1
			for i in range(3):
				try:
					if column+(i-1) >= 0:
						grid[row][column+(i-1)] = 3
					if DEBUG > 1 and DEBUG < 2: print(row,column+(i-1))
				except:
					print("Error",row,column)		
		else:
			if DEBUG > 1 and DEBUG < 2: print("Can't attack",x,y,player,direction)
			
			
	if direction == "left":
		if DEBUG > 1 and DEBUG < 2: print("ARGS:",x,y,player,direction)
		if column >= LIMIT_UL:
		
			column -= 1
			for i in range(3):
				try:
					if row+(i-1) >= 0:
						grid[row+(i-1)][column] = 3
					if DEBUG > 1 and DEBUG < 2: print(row+(i-1),column)
				except:
					print("Error",row,column)
		else:
			if DEBUG > 1 and DEBUG < 2: print("Can't attack",x,y,player,direction)
			
			
	if direction == "right":
		if DEBUG > 1 and DEBUG < 2: print("ARGS:",x,y,player,direction)
		if column <= LIMIT_DR:
		
			column += 1
			for i in range(3):
				try:
					if row+(i-1) >= 0:
						grid[row+(i-1)][column] = 3
					if DEBUG > 1 and DEBUG < 2: print(row+(i-1),column)
				except:
					print("Error",row,column)
		else:
			if DEBUG > 1 and DEBUG < 2: print("Can't attack",x,y,player,direction)
	return FPS * 0.4

# -------- Main Program Loop -----------
while not done:
	pressed = pygame.key.get_pressed()


	if pressed[pygame.K_UP]:
		move("up",pos[0],pos[1])
		direction = "up"

	if pressed[pygame.K_DOWN]:
		move("down",pos[0],pos[1])
		direction = "down"

	if pressed[pygame.K_LEFT]:
		move("left",pos[0],pos[1])
		direction = "left"
	if pressed[pygame.K_RIGHT]:
		move("right",pos[0],pos[1])
		direction = "right"
	# if pressed[pygame.K_SPACE]:
		# attack(pos[0],pos[1],"human")

	for event in pygame.event.get():  # User did something
		if event.type == pygame.QUIT:  # If user clicked close
			done = True
		if pressed[pygame.K_ESCAPE]:
			done = True# Flag that we are done so we exit this loop
		if pressed[pygame.K_SPACE]:
			timer = attack(pos[0],pos[1],"human",direction)
	if DEBUG == 3: print(c_ai_pos.__dict__)
	tmp_ai = pick_square_ai(c_ai_pos.x,c_ai_pos.y)
	
	if grid[x2grid(tmp_ai[0])][x2grid(tmp_ai[1])] == 0:
		c_ai_pos.update_ai(tmp_ai[0],tmp_ai[1])
		grid[c_ai_pos.row][c_ai_pos.col] = 2
		grid[c_ai_pos.l_row][c_ai_pos.l_col] = 0
	if grid[x2grid(tmp_ai[0])][x2grid(tmp_ai[1])] == 1:
		print("OCCUPIED!")
	
	

	if timer > 0:
		timer -= 1
	if timer == 0:
		for row in range(MATRIX):
			for column in range(MATRIX):
				if grid[row][column] == 3:
					grid[row][column] = 0
	# Set the screen background
	screen.fill(BLACK)
	if DEBUG == 2: print(timer)
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
					color = RED
					if DEBUG == 2: print("white")
				else:
					color = BLACK
					print(timer%2)
					if DEBUG == 2: print("black")

				#color = WHITE
			#pygame.time.wait(10)
			pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN, WIDTH,HEIGHT])


	# Limit to FPS var
	clock.tick(FPS)


	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
