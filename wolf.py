from animal import Animal

class WolfConfig:
    default_max_health = 100    
    reproduction_health = 50
    reset_health = 20    
    initial_health = 10
    move_distance = 1
    sheep_health_bonus = 10

    def __init__(self, max_health = default_max_health, 
                 reset_health = reset_health, 
                 initial_health = initial_health, 
                 sheep_health_bonus = sheep_health_bonus, 
                 reproduction_health = reproduction_health, 
                 move_distance = move_distance):
        self.max_health = max_health
        self.reset_health = reset_health
        self.initial_health = initial_health
        self.sheep_health_bonus = sheep_health_bonus
        self.reproduction_health = reproduction_health
        self.max_health = move_distance
        
    
class Wolf(Animal):
    def __init__(self, x, y, min_x, min_y, max_x, max_y, sheep, wolf_config):
        super().__init__(x=x, y=y, min_x = min_x, min_y = min_y, max_x = max_x, max_y = max_y)
        self.sheep = sheep
        self.config = wolf_config
        self.health = wolf_config.initial_health
        self.move_distance = wolf_config.move_distance

    def do_turn(self):
        self.age()
        if self.is_alive():
            self.feed()
            self.move()
            self.reproduce()

    def age(self):
        self.health = self.health - 1
        if self.health <= 0:
            self.die()

    def feed(self):
        for i in range(len(self.sheep)):
            if self.x == self.sheep[i].x and self.y == self.sheep[i].y:
                self.sheep[i].state = Animal.STATE_DEAD
                self.health = self.health + self.config.sheep_health_bonus

    def choose_max_food_direction(self):
        for i in range(len(self.sheep)):
            if abs(self.x - self.sheep[i].x) < 2 and abs(self.y - self.sheep[i].y) < 2:
                return True, self.sheep[i].x, self.sheep[i].y
        return False, 0, 0

    def move(self):
        found_food, new_x, new_y = self.choose_max_food_direction()
        if found_food:
            self.x = new_x
            self.y = new_y
        else:
            self.random_move()

    def reproduce(self):
        if self.health > self.config.reproduction_health:
            self.offspring = self.offspring + 1
            self.health = self.config.reset_health

