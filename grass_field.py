import random
import numpy as np
import sheep


class GrassFieldConfig:

    spread_threshold = 3
    grass_growth_rate = 0.2
    max_grass = 9
    growth_probability = 10.2   
    spread_probability = 0.1    

    def __init__(self, spread_threshold = spread_threshold,
        grass_growth_rate = grass_growth_rate,
        max_grass = max_grass,
        growth_probability = growth_probability,
        spread_probability = spread_probability):
        
        self.spread_threshold = spread_threshold
        self.grass_growth_rate = grass_growth_rate
        self.max_grass = max_grass
        self.growth_probability = growth_probability
        self.spread_probability = spread_probability


        


class GrassField:
    def __init__(self, width, height, grass_field_config):
        self.width = width
        self.height = height
        self.config = grass_field_config

        self.grass_amount = np.zeros((width,height))
        self.propagules = np.zeros((width, height))
       
    def text_symbol(self, x, y):
        if self.grass_field.grass_amount[x,y] == 0:
            return "   "
        if self.grass_field.grass_amount[x,y] < 2:
            return " 🌱 "
        if self.grass_field.grass_amount[x,y] < 5:
            return " 🌿 "
        if self.grass_field.grass_amount[x,y] < 9:
            return "🌿🌿🌿"
        return "🌾🌾🌾"
        

    def grow_grass(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.grass_amount[x,y] > 0: 
                    if random.random() < self.config.growth_probability:
                        self.grass_amount[x,y] = min(self.grass_amount[x,y] + self.config.grass_growth_rate, self.config.max_grass)

    def spread_grass(self):
        self.propagules = np.zeros((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                if self.grass_amount[x,y] >= self.config.spread_threshold:
                    self.__spread_grass_at(x,y)
        self.propagules = np.clip(self.propagules, 0, 1)
        self.grass_amount = np.add(self.grass_amount, self.propagules)
        self.grass_amount = np.clip(self.grass_amount, 0, self.config.max_grass)

    
    def __spread_grass_at(self, x, y):
        if x > 0 and random.random() < self.config.spread_probability:
            self.propagules[x-1,y] = self.propagules[x-1,y] + 1
        if x + 1 < self.width and random.random() < self.config.spread_probability:
            self.propagules[x+1,y] = self.propagules[x+1,y] + 1 
        if y > 0 and random.random() < self.config.spread_probability:
            self.propagules[x,y-1] = self.propagules[x,y-1] + 1
        if y < self.height - 1 and random.random() < self.config.spread_probability:
            self.propagules[x,y+1] = self.propagules[x,y+1] + 1


    def create_grass_at(self, x, y, grass_amount):
        self.grass_amount[x,y] = grass_amount
    


