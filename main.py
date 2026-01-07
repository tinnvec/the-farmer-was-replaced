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
clear()

num_hay = 0
num_wood = 0
num_carrots = 0

num_water = 0
num_fertilizer = 0

current_ground_type = None
current_water_level = 0

while True:
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			num_fertilizer = num_items(Items.Fertilizer)

			while not can_harvest():
				if num_fertilizer > 0:
					use_item(Items.Fertilizer)
					num_fertilizer = num_items(Items.Fertilizer)
				else:
					continue

			harvest()

			current_ground_type = get_ground_type()

			num_hay = num_items(Items.Hay)
			num_wood = num_items(Items.Wood)
			num_carrots = num_items(Items.Carrot)

			if num_hay > num_carrots and num_wood > num_carrots:
				if get_ground_type() != Grounds.Soil:
					till()

				if not plant(Entities.Carrot):
					plant(Entities.Bush)
			elif num_hay > num_wood and num_carrots > num_wood:
				if (x + y) % 2 == 0:
					plant(Entities.Tree)
				else:
					plant(Entities.Bush)
			elif get_ground_type() != Grounds.Grassland:
				till()

			current_water_level = get_water()
			num_water = num_items(Items.Water)

			if num_water > 0 and current_water_level < 0.25:
				use_item(Items.Water)

			move(North)
		move(East)
