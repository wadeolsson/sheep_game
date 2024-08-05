import random

         
def random_cell_within(distance, x, y, max_x, max_y):
    new_x = x+random.randint(-1*distance,distance)
    new_y = y+random.randint(-1*distance,distance)
    if new_x < 0:
        new_x = 0
    if new_x >= max_x:
        new_x = max_x
    if new_y < 0:
        new_y = 0
    if new_y >= max_y:
        new_y = max_y
    return new_x, new_y
