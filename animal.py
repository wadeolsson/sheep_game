import util

class Animal:
    STATE_DEAD = "dead"
    STATE_ALIVE = "alive"

    def __init__(self, x, y, min_x, min_y, max_x, max_y, move_distance = 1):
        self.state = Animal.STATE_ALIVE
        self.x = x
        self.y = y
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.move_distance = move_distance
        self.offspring = 0

    def is_alive(self):
        return self.state == Animal.STATE_ALIVE

    def is_dead(self):
        return self.state == Animal.STATE_DEAD
    
    def has_offspring(self):
        return self.offspring > 0
    
    def get_move_distance(self):
        return self.move_distance
    
    def random_move(self):
        moved = False
        move_tries = 0                    
        self.x, self.y = util.random_cell_within(self.get_move_distance(), self.x, self.y, self.min_x, self.min_y, self.max_x, self.max_y)

    def die(self):
        self.state = Animal.STATE_DEAD
