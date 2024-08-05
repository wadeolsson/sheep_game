class Animal:
    STATE_DEAD = "dead"
    STATE_ALIVE = "alive"

    offspring = 0
    state = STATE_ALIVE

    def __init__(self):
        self.state = Animal.STATE_ALIVE
        self.offspring = 0

    def is_alive(self):
        return self.state == Animal.STATE_ALIVE

    def is_dead(self):
        return self.state == Animal.STATE_DEAD
    
    def has_offspring(self):
        return self.offspring > 0
