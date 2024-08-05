import random

         
def random_cell_within(distance, x, y, min_x, min_y, max_x, max_y):
    new_x = x+random.randint(-1*distance,distance)
    new_y = y+random.randint(-1*distance,distance)
    if new_x < min_x:
        new_x = min_x
    if new_x > max_x:
        new_x = max_x
    if new_y < min_y:
        new_y = min_y
    if new_y > max_y:
        new_y = max_y
    return new_x, new_y


