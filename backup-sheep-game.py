import numpy as np
import time
import random

## wolf 🐕
# rock 🪨

width = 48 
height = 24
spread_threshold = 3
grass_growth_rate = 3  # default 1
max_grass = 9   # default 9 (Dont change, changing doesnt do anything)
max_sheep = 1000 # default 500
graze_amount = 2    # default 2
initial_delay = 15  # default 20
growth_probability = 0.2    # default 0.1
spread_probability = 0.3    # default 0.2
sleep_amount = 0.07   # default 0.1
sheep_death_chance = 0.05   # default 0.1
max_health = 20     # default 20
reproduction_health = 15    # default 15
sheep_reset_health = 10     # default 10
initial_x = 10      # default 10    Controls initial sheep spawnpoint
initial_y = 10      # default 10
iterations = 0      # default 0

class Sheep:
    def __init__(self, x, y, min_x, min_y, max_x, max_y, field):
        self.x = x
        self.y = y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.field = field
        self.health = initial_health
        
    def kill_sheep(self):
        del self.self
    
    def get_max_field_dir(self):
        max = self.field.field[self.x,self.y]
        dir_x = 0
        dir_y = 0
        if self.y+1 < self.max_y and self.field.field[self.x, self.y+1] > max:
            dir_x = 0
            dir_y = 1
            max = self.field.field[self.x + dir_x, self.y + dir_y]
        if self.y+1 < self.max_y and self.x+1 < self.max_x and self.field.field[self.x+1, self.y+1] > max:
            dir_x = 1
            dir_y = 1
            max = self.field.field[self.x + dir_x, self.y + dir_y]
        if self.x+1 < self.max_x and self.field.field[self.x+1, self.y] > max:
            dir_x = 1
            dir_y = 0
            max = self.field.field[self.x + dir_x, self.y + dir_y]
        if self.y-1 > self.min_y and self.x+1 < self.max_x and self.field.field[self.x+1, self.y-1] > max:
            dir_x = 1
            dir_y = -1
            max = self.field.field[self.x + dir_x, self.y + dir_y]
        if self.y-1 > self.min_y and self.field.field[self.x, self.y-1] >0 :
            dir_x = 0
            dir_y = -1
            max = self.field.field[self.x + dir_x, self.y + dir_y]
        if self.y-1 > self.min_y and self.x-1 < self.min_x and self.field.field[self.x-1, self.y-1] > max:
            dir_x = -1
            dir_y = -1
            max = self.field.field[self.x + dir_x, self.y + dir_y]
        if self.x-1 > self.min_x and self.field.field[self.x-1, self.y] >0 :
            dir_x = -1
            dir_y = 0
            max = self.field.field[self.x + dir_x, self.y + dir_y]
        if self.y+1 < self.max_y and self.x-1 < self.min_x and self.field.field[self.x-1, self.y+1] > max:
            dir_x = -1
            dir_y = 1
        if max == 0:
            return False, 0, 0

        return True, dir_x, dir_y

    def roam(self):
        found_food, dir_x, dir_y = self.get_max_field_dir()
        if found_food:
            self.x = self.x + dir_x
            self.y = self.y + dir_y
        else:
            self.random_move()

    def random_move(self):
        moved = False
        move_tries = 0
        while not moved and move_tries < 5:
            move_tries = move_tries + 1
            dir = random.randint(1,4)
            if dir == 1:
                if self.x > self.min_x + 1:
                    self.x = self.x - 1
                    moved = True
            elif dir == 2:
                if self.x < self.max_x - 1:
                    self.x = self.x + 1
                    moved = True
            elif dir == 3:
                if self.y > self.min_y + 1:
                    self.y = self.y - 1
                    moved = True
            elif dir == 4:
                if self.y < self.max_y - 1:
                    self.y = self.y + 1
                    moved = True
            else:
                print("uh oh, bad direction")
        

field = GrassField(width, height)
field.create_grass_at(initial_x, initial_y, 1)
turns = 0
cont = True
while cont == True:
    turns = turns + 1
    if turns == initial_delay:
        # field.create_sheep_at(random.randint(0,width-1),random.randint(0,height-1))
        field.create_sheep_at(initial_x, initial_y)
    field.print_field()
    field.grow_grass()
    field.spread_grass()
    field.do_sheep_things()
    field.print_stats()
    time.sleep(sleep_amount)
    iterations = iterations + 1
    print('iterations:',iterations)
    cont = field.check_end()
    

