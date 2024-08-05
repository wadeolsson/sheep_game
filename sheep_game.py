import numpy as np
import time
import grass_field
from sheep import Sheep, SheepConfig
import util

## wolf 🐕
# rock 🪨

width = 20
height = 20
max_sheep = 1000 # default 500
initial_x = 10
initial_y = 10

initial_delay = 15  # default 20
sleep_amount = 0.07   # default 0.1

# sheep_death_chance = 0.05   # default 0.1

class SheepGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sheep = []
        self.grass_field = grass_field.GrassField(width, height)
        self.iterations = 0

    def text_symbol_grass(self, x, y):
        if self.grass_field.grass_amount[x,y] == 0:
            return "   "
        if self.grass_field.grass_amount[x,y] < 2:
            return " 🌱 "
        if self.grass_field.grass_amount[x,y] < 5:
            return " 🌿 "
        if self.grass_field.grass_amount[x,y] < 9:
            return "🌿🌿🌿"
        return "🌾🌾🌾"
        

    def text_symbol_sheep(self, x, y):
        for i in range(len(self.sheep)):
            sheep = self.sheep[i]
            if x == sheep.x and y == sheep.y:
                return "🐑"
        return " "


    def print_field(self):
        for x in range(self.width):
            for y in range(self.height):
                print("{}{}".format(self.text_symbol_grass(x,y), self.text_symbol_sheep(x,y)), end="")
            print()

    def do_grass_things(self):
        self.grass_field.grow_grass()
        self.grass_field.spread_grass()

    def create_sheep_at(self, x, y):
        sheep_config = SheepConfig()
        new_sheep = Sheep(x, y, 0, 0, self.width, self. height, self.grass_field, sheep_config)
        self.sheep.append(new_sheep)
        self.sheep_spawned = True
    
    def do_sheep_things(self):
        if self.iterations == initial_delay:
            self.create_sheep_at(initial_x, initial_y)

        dead_sheep = []
        for i in range(len(self.sheep)):
            my_sheep = self.sheep[i]
            my_sheep.do_turn()
            if my_sheep.is_dead(): 
                dead_sheep.append(my_sheep)
            if my_sheep.has_offspring():
                for i in range(my_sheep.offspring):
                    new_x, new_y = util.random_cell_within(2, my_sheep.x, my_sheep.y, self.width-1, self.height-1)
                    self.create_sheep_at(new_x,new_y)
                my_sheep.offspring = 0

        for i in range(len(dead_sheep)):
            self.sheep.remove(dead_sheep[i])

    def print_stats(self):
        print('iterations: {}',self.iterations)
        print('sheep:      {}'.format(len(self.sheep)))
        print('grass:      {}'.format(np.concatenate(self.grass_field.grass_amount).sum()))

    def check_end(self):
        if self.iterations > initial_delay:
            if len(self.sheep) == 0:
                return False
        return True
            
    def execute(self):
        self.iterations = 0
        cont = True
        while cont == True:
            self.iterations = self.iterations + 1
            game.do_grass_things()
            game.do_sheep_things()

            game.print_field()
            game.print_stats()
            time.sleep(sleep_amount)
            cont = game.check_end()
        
game = SheepGame(width, height)
game.grass_field.create_grass_at(initial_x, initial_y, 1)
game.execute()
    

