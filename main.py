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
	#print(exits) #debugging purposes
	minons = make_minions(rng)
	
	object_list = ["Gold","Silver","Trash","wood","Iron","Leather","cloth","Potion","Meal","Water","Special"]
	inv = {}
	for x in object_list:
		inv[x] = random.randint(0,4)
	#print(inv) #debugging purposes only
	return exits
	
def make_minions(rng):
	#save this space for the make enemy function
	
	enemy_list = ["Goblin","Rats","Giant rat","Snail","zombie","Vampire","Ghost","witch","Org","Orc","Special"]
	enmy_aval = {}
	n_e_list = random.sample(enemy_list,rng)
	
	for q in n_e_list:
		int = random.randint(0,5)
		if int > 0:
			enmy_aval[q] = int
	print(enmy_aval) #debugging purposes only
	print(give_minion_stats(enmy_aval))
	

def give_minion_stats(dict):
	q = 1;
	minion_stats = {}
	for i in dict:
		print("{} {}".format(i, dict[i])) #debugging purposes 
		p = 0 # THIS IS OUR PROBLEM!	
		while p < dict[i]:
		 		
			minion = { "Name": i, "ID": q, "HP": random.randint(25,100)}
			#minion_stats[q] = {}
			minion_stats[q] = minion
			p += 1
			q += 1
	
	return minion_stats
#make_wait()
#clear_wait()
print(make_room(1,3))