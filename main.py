clear()

while True:
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if can_harvest():
				harvest()
				#plant(Entities.Bush)
			move(North)
		move(East)