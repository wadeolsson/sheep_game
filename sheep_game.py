import numpy as np
import time
from grass_field import GrassField, GrassFieldConfig
from sheep import Sheep, SheepConfig
from wolf import Wolf, WolfConfig
import util

iteration_first_sheep = 40
iteration_first_wolf = 100

sheep_config = SheepConfig(
    max_health = 100,
    graze_amount = 2,
    reproduction_health = 15,
    reset_health = 10,
    initial_health = 10,
    move_distance = 1
)

wolf_config = WolfConfig(
    max_health = 50,    
    reproduction_health = 50,
    reset_health = 10, 
    initial_health = 20,
    move_distance = 1,
    sheep_health_bonus = 10
)

grass_field_config = GrassFieldConfig(
    spread_threshold = 3,
    grass_growth_rate = 0.2,
    max_grass = 9,
    growth_probability = 10.2,   
    spread_probability = 0.1    
)

width = 20
height = 20

initial_x = 10
initial_y = 10

sleep_amount = 0.07   # default 0.1

SYMBOL_GRASS_0 = "  "
SYMBOL_GRASS_1 = " 🌱"
SYMBOL_GRASS_2 = " 🌿"
SYMBOL_GRASS_3 = "🌿🌿"
SYMBOL_GRASS_4 = "🌾🌾"
SYMBOL_SHEEP = "🐑"
SYMBOL_WOLF_1 = "🐺"
SYMBOL_WOLF_2 = "🐕"


class SheepGame:
    def __init__(self, width, height, grass_field_config, sheep_config, wolf_config):
        self.width = width
        self.height = height
        self.min_x = 0
        self.min_y = 0
        self.max_x = self.width - 1
        self.max_y = self.height - 1
        self.grass_field_config = grass_field_config
        self.sheep_config = sheep_config
        self.wolf_config = wolf_config

        self.sheep = []
        self.wolves = []
        self.grass_field = GrassField(width, height, grass_field_config)
        self.iterations = 0


    def text_symbol_grass(self, x, y):
        if self.grass_field.grass_amount[x,y] == 0:
            return SYMBOL_GRASS_0
        if self.grass_field.grass_amount[x,y] < 2:
            return SYMBOL_GRASS_1
        if self.grass_field.grass_amount[x,y] < 5:
            return SYMBOL_GRASS_2
        if self.grass_field.grass_amount[x,y] < 9:
            return SYMBOL_GRASS_3
        return SYMBOL_GRASS_4
        
    def sheep_at(self,x,y):
        for i in range(len(self.sheep)):
            sheep = self.sheep[i]
            if x == sheep.x and y == sheep.y:
                return sheep
        return None       
    
    def wolf_at(self,x,y):
        for i in range(len(self.wolves)):
            wolf = self.wolves[i]
            if x == wolf.x and y == wolf.y:
                return wolf
        return None
    
    def print_field(self):
        for x in range(self.width):
            for y in range(self.height):
                symbol=self.text_symbol_grass(x,y)
                if self.wolf_at(x,y):
                    symbol = symbol[0] + SYMBOL_WOLF_1
                elif self.sheep_at(x,y):
                    symbol= symbol[0] + SYMBOL_SHEEP
                print("{}".format(symbol), end="")
            print()

    def do_grass_things(self):
        self.grass_field.grow_grass()
        self.grass_field.spread_grass()

    def do_wolf_things(self):
        if self.iterations == iteration_first_wolf:
            self.create_wolf_at(initial_x, initial_y)
        dead_wolves = []
        for i in range(len(self.wolves)):
            my_wolf = self.wolves[i]
            my_wolf.do_turn()
            if my_wolf.is_dead(): 
                dead_wolves.append(my_wolf)
            if my_wolf.has_offspring():
                for i in range(my_wolf.offspring):
                    new_x, new_y = util.random_cell_within(1, my_wolf.x, my_wolf.y, self.min_x, self.min_y, self.max_x, self.max_y)
                    self.create_wolf_at(new_x,new_y)
                my_wolf.offspring = 0

        for i in range(len(dead_wolves)):
            self.wolves.remove(dead_wolves[i])

    def create_sheep_at(self, x, y):
        sheep_config = self.sheep_config
        new_sheep = Sheep(x, y, self.min_x, self.min_y, self.max_x, self. max_y, self.grass_field, sheep_config)
        self.sheep.append(new_sheep)
    
    def create_wolf_at(self, x, y):
        wolf_config = self.wolf_config
        new_wolf = Wolf(x, y, self.min_x, self.min_y, self.max_x, self. max_y, self.sheep, wolf_config)
        self.wolves.append(new_wolf)
    
    def do_sheep_things(self):
        if self.iterations == iteration_first_sheep:
            self.create_sheep_at(initial_x, initial_y)

        dead_sheep = []
        for i in range(len(self.sheep)):
            my_sheep = self.sheep[i]
            my_sheep.do_turn()
            if my_sheep.is_dead(): 
                dead_sheep.append(my_sheep)
            if my_sheep.has_offspring():
                for i in range(my_sheep.offspring):
                    new_x, new_y = util.random_cell_within(2, my_sheep.x, my_sheep.y, self.min_x, self.min_y, self.max_x, self.max_y)
                    self.create_sheep_at(new_x,new_y)
                my_sheep.offspring = 0

        for i in range(len(dead_sheep)):
            self.sheep.remove(dead_sheep[i])

    def print_stats(self):
        print('iterations: {}'.format(self.iterations))
        print('sheep:      {}'.format(len(self.sheep)))
        print('wolves:     {}'.format(len(self.wolves)))
        print('grass:      {}'.format(np.concatenate(self.grass_field.grass_amount).sum()))

    def check_end(self):
        if self.iterations > iteration_first_sheep:
            if len(self.sheep) == 0:
                return False
        if self.iterations > iteration_first_wolf:
            if len(self.wolves) == 0:
                return False
        return True
            
    def execute(self):
        self.iterations = 0
        cont = True
        while cont == True:
            self.iterations = self.iterations + 1
            game.do_grass_things()
            game.do_sheep_things()
            game.do_wolf_things()

            game.print_field()
            game.print_stats()
            time.sleep(sleep_amount)
            cont = game.check_end()
        

game = SheepGame(width, height, grass_field_config, sheep_config, wolf_config)
game.grass_field.create_grass_at(initial_x, initial_y, 1)
game.execute()
    

