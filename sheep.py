import random
from animal import Animal

class SheepConfig:
    max_health = 20     # default 20
    graze_amount = 2    # default 2
    reproduction_health = 15
    reset_health = 10     # default 10
    initial_health = 10

class Sheep(Animal):
    def __init__(self, x, y, min_x, min_y, max_x, max_y, grass_field, sheep_config):
        self.x = x
        self.y = y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.health = sheep_config.initial_health
        self.grass_field = grass_field
        self.config = sheep_config
        self.state = Animal.STATE_ALIVE
    
    def graze(self):
        grazed_amount = min(self.grass_field.grass_amount[self.x,self.y], self.config.graze_amount)
        self.grass_field.grass_amount[self.x,self.y] = max(0, self.grass_field.grass_amount[self.x,self.y] - self.config.graze_amount)
        self.health = self.health + grazed_amount

    
    def choose_max_food_direction(self):
        max = self.grass_field.grass_amount[self.x,self.y]
        dir_x = 0
        dir_y = 0
        if self.y+1 < self.max_y and self.grass_field.grass_amount[self.x, self.y+1] > max:
            dir_x = 0
            dir_y = 1
            max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
        if self.y+1 < self.max_y and self.x+1 < self.max_x and self.grass_field.grass_amount[self.x+1, self.y+1] > max:
            dir_x = 1
            dir_y = 1
            max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
        if self.x+1 < self.max_x and self.grass_field.grass_amount[self.x+1, self.y] > max:
            dir_x = 1
            dir_y = 0
            max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
        if self.y-1 > self.min_y and self.x+1 < self.max_x and self.grass_field.grass_amount[self.x+1, self.y-1] > max:
            dir_x = 1
            dir_y = -1
            max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
        if self.y-1 > self.min_y and self.grass_field.grass_amount[self.x, self.y-1] >0 :
            dir_x = 0
            dir_y = -1
            max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
        if self.y-1 > self.min_y and self.x-1 < self.min_x and self.grass_field.grass_amount[self.x-1, self.y-1] > max:
            dir_x = -1
            dir_y = -1
            max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
        if self.x-1 > self.min_x and self.grass_field.grass_amount[self.x-1, self.y] >0 :
            dir_x = -1
            dir_y = 0
            max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
        if self.y+1 < self.max_y and self.x-1 < self.min_x and self.grass_field.grass_amount[self.x-1, self.y+1] > max:
            dir_x = -1
            dir_y = 1
        if max == 0:
            return False, 0, 0

        return True, dir_x, dir_y
    
    def roam(self):
        found_food, dir_x, dir_y = self.choose_max_food_direction()
        if found_food:
            self.x = self.x + dir_x
            self.y = self.y + dir_y
        else:
            self.random_move()

    def text_symbol(self):
        return "🐑"

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

    def die(self):
        self.state = Animal.STATE_DEAD
    
    def do_turn(self):
        self.health = self.health - 1
        self.graze()
        if self.health <= 0:
            self.die()
        if self.grass_field.grass_amount[self.x, self.y] == 0:
            self.roam()
        if self.health > self.config.reproduction_health:
            self.offspring = self.offspring + 1
            self.health = self.config.reset_health
    
        