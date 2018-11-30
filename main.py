#!/usr/bin/env python3 
import time
import random
def make_wait():
	for x in range (0,5):  
		b = "Loading" + "." * x
		print (b, end="\r")
		time.sleep(0.5)
def clear_wait():
	print("\r						\r")

def entrance_to_exit(int):
	if int <= 2:
		int = int + 2
	else:
		int = int - 2
	return int
		
	
def make_room(entrance,rng):

	#Creates a set of exits for the room
	exits = [entrance_to_exit(entrance)]
	for i in range(1,random.randint(1,4)):
		random_check = random.randint(1,4)
		if random_check not in exits:
			exits.append(random_check)
	
	#save this space for the make enemy function
	
	objects = random.randint(0,5)

make_wait()
clear_wait()
make_room(1,1)