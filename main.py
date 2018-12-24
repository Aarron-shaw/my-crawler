#!/usr/bin/env python3 
import time
import random
					\r")

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
	

class minion_stats(object):
	def __init__(self,name,id,hp,level,attack,defense):
		self.name = name
		self.id = id
		self.hp = hp
		self.level = level
		self.attack = attack
		self.defense = defense
		
	
	
#make_wait()
#clear_wait()
print(make_room(1,3))