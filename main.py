from __builtins__ import *

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
