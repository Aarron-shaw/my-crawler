#!/usr/bin/env python3 
import random

enemy_list = ["Goblin","Rats","Giant rat","Snail","zombie","Vampire","Ghost","witch","Org","Orc","Special"]

class minion_stats(object):
	def __init__(self,name,id,hp,level,attack,defense):
		self.name = name
		self.id = id
		self.hp = hp
		self.level = level
		self.attack = attack
		self.defense = defense
	
	
def make_minion(q):

	name = enemy_list[random.randint(0,10)]
	hp = random.randint(10,100)
	id = q
	level = 1
	attack = random.randint(1,10)
	defense = random.randint(1,10)
	first = minion_stats(name,id,hp,level,attack,defense)
	return first

	
q = 1
i = 0
minion = list()
while i < len(enemy_list):
	minion.append(make_minion(q))
	q += 1
	i += 1
	
print(minion)
		
