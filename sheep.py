import random
from animal import Animal
import util

class SheepConfig:
    max_health = 100     # default 20
    graze_amount = 2    # default 2
    reproduction_health = 40
    reset_health = 20     # default 10
    initial_health = 10
    move_distance = 1
    
    def __init__(self, max_health = max_health, 
                 reset_health = reset_health, 
                 initial_health = initial_health, 
                 graze_amount = graze_amount, 
                 reproduction_health = reproduction_health, 
                 move_distance = move_distance):
        self.max_health = max_health
        self.reset_health = reset_health
        self.initial_health = initial_health
        self.graze_amount = graze_amount
        self.reproduction_health = reproduction_health
        self.max_health = move_distance
        

class Sheep(Animal):
    def __init__(self, x, y, min_x, min_y, max_x, max_y, grass_field, sheep_config):
        super().__init__(x=x, y=y, min_x = min_x, min_y = min_y, max_x = max_x, max_y = max_y)
        self.health = sheep_config.initial_health
        self.move_distance = sheep_config.move_distance
        self.grass_field = grass_field
        self.config = sheep_config
    
    def graze(self):
        grazed_amount = min(self.grass_field.grass_amount[self.x,self.y], self.config.graze_amount)
        self.grass_field.grass_amount[self.x,self.y] = max(0, self.grass_field.grass_amount[self.x,self.y] - self.config.graze_amount)
        self.health = self.health + grazed_amount

    
    def choose_max_food_direction(self):
        max = self.grass_field.grass_amount[self.x,self.y]
        dir_x = 0
        dir_y = 0
        for x in range(-1,1):
            for y in range(-1,1):
                if self.x + x >= self.min_x and self.x + x <= self.max_x and self.y + y >= self.min_y and self.y + y <= self.max_y:
                    if self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y] > max:
                        dir_x = x
                        dir_y = y
                        max = self.grass_field.grass_amount[self.x + dir_x, self.y + dir_y]
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

    def get_move_distance(self):
        return self.move_distance

    
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
    
        