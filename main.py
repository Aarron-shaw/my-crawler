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

def make_room(rng):
	exits = []
	for i in range(1,4):
		random_check = random.randint(1,4)
		if random_check not in exits:
			exits.append(random_check)
	
	#save this space for the make enemy function
	
	objects = random.randint(0,5)

make_wait()
clear_wait()
make_room(1)