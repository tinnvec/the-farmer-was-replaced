from __builtins__ import *

def move_to(x, y):
	world_size = get_world_size()

	current_x = get_pos_x()
	current_y = get_pos_y()
	
	if x > current_x:
		x_dir = 1
	else:
		x_dir = -1
	if abs(x - current_x) > world_size / 2:
		x_dir *= -1

	if x_dir > 0:
		x_dir = East
	else:
		x_dir = West
	
	if y > current_y:
		y_dir = 1
	else:
		y_dir = -1
	if abs(y - current_y) > world_size / 2:
		y_dir *= -1

	if y_dir > 0:
		y_dir = North
	else:
		y_dir = South

	while get_pos_x() != x:
		move(x_dir)

	while get_pos_y() != y:
		move(y_dir)

def do_harvest():
	if get_entity_type() == None:
		return

	num_fertilizer = num_items(Items.Fertilizer)
	while not can_harvest():
		if num_fertilizer > 0:
			use_item(Items.Fertilizer)
			num_fertilizer = num_items(Items.Fertilizer)
		else:
			continue

	harvest()

def do_water():
	current_water_level = get_water()
	num_water = num_items(Items.Water)

	if num_water > 2 and current_water_level < 0.25:
		use_item(Items.Water, 3)

def harvest_hay():
	world_size = get_world_size()

	move_to(0, 0)
	for x in range(world_size):
		for y in range(world_size):
			do_harvest()
			if get_ground_type() != Grounds.Grassland:
				till()
			do_water()
			move(North)
		move(East)

def harvest_wood():
	world_size = get_world_size()

	move_to(0, 0)
	for x in range(world_size):
		for y in range(world_size):
			do_harvest()
			if (x + y) % 2 == 0:
				plant(Entities.Tree)
			else:
				plant(Entities.Bush)
			do_water()
			move(North)
		move(East)

def harvest_carrots():
	world_size = get_world_size()

	move_to(0, 0)
	for x in range(world_size):
		for y in range(world_size):
			do_harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Carrot)
			do_water()
			move(North)
		move(East)

def harvest_pumpkins():
	world_size = get_world_size()

	# Till/plant whole field
	move_to(0, 0)
	for x in range(world_size):
		for y in range(world_size):
			do_harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
			do_water()
			move(North)
		move(East)
	
	# Replant fails, keep track
	failed_plants = []
	move_to(0, 0)
	for x in range(world_size):
		for y in range(world_size):
			if not can_harvest():
				plant(Entities.Pumpkin)
				failed_plants.append([x, y])
			move(North)
		move(East)

	# Recheck fails until none
	while len(failed_plants) > 0:
		position = failed_plants.pop(0)
		move_to(position[0], position[1])
		if not can_harvest():
			plant(Entities.Pumpkin)
			failed_plants.append(position)
	
	move_to(0, 0)
	harvest()

clear()

num_hay = 0
num_wood = 0
num_carrots = 0

num_water = 0
num_fertilizer = 0

current_ground_type = None
current_water_level = 0

while True:
	world_size = get_world_size()

	num_hay = num_items(Items.Hay)
	num_wood = num_items(Items.Wood)
	num_carrots = num_items(Items.Carrot)
	num_pumpkins = num_items(Items.Pumpkin)

	if num_carrots > world_size ** 2 and num_hay > num_pumpkins and num_wood > num_pumpkins and num_carrots > num_pumpkins:
		harvest_pumpkins()
	elif num_hay / 4 > world_size ** 2 and num_wood / 4 > world_size ** 2 and num_hay > num_carrots and num_wood > num_carrots and num_pumpkins > num_carrots:
		harvest_carrots()
	elif num_hay > num_wood and num_carrots > num_wood and num_pumpkins > num_wood:
		harvest_wood()
	else:
		harvest_hay()
