import arcade.key
from random import randint, random

DIR_HORIZONTAL = 0
DIR_VERTICAL = 1

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0
    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class Asteroid(Model):
    def __init__(self, world, x, y, vx, vy):
        super().__init__(world, x, y, 0)
        self.vx = vx
        self.vy = vy
        self.angle = randint(0,359)

    def random_direction(self):
        self.vx = 5 * random()
        self.vy = 5 * random()
        
    def animate(self, delta):
        if (self.x < 0) or (self.x > self.world.width):
            self.vx = - self.vx
        
        if (self.y < 0) or (self.y > self.world.height):
            self.vy = - self.vy
        
        self.x += self.vx
        self.y += self.vy
        self.angle += 3
    


class Ship(Model):

    DIR_HORIZONTAL = 0
    DIR_VERTICAL = 1
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.direction = Ship.DIR_VERTICAL
    
    def switch_direction(self):
        if self.direction == Ship.DIR_HORIZONTAL:
            self.direction = Ship.DIR_VERTICAL
            self.angle = 0
        else:
            self.direction = Ship.DIR_HORIZONTAL
            self.angle = -90


    def update(self, delta):
        if self.direction == Ship.DIR_VERTICAL:
            if self.y > self.world.height:
                self.y = 0
            self.y += 5
        else:
            if self.x > self.world.width:
                self.x = 0
            self.x += 5


class World():
    NUM_ASTEROID = 10
    def __init__(self, window, width, height):
        
        self.width = width
        self.height = height

        self.window = window

        self.ship = Ship(self,100, 100)
        self.gold = Gold(self, 400, 400)
        self.asteroids = []
        for i in range(World.NUM_ASTEROID):
            asteroid = Asteroid(self, 0, 0, 0, 0)
            asteroid.random_direction()
            self.asteroids.append(asteroid)
        self.score = 0

    
    def addAsteriod(self, key, key_modifiers):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.switch_direction()

        if key == arcade.key.Z:
            self.NUM_ASTEROID += 1
            asteroid = Asteroid(self, 0, 0, 0, 0)
            asteroid.random_direction()
            self.asteroids.append(asteroid)
            self.window.insert_asteroid(asteroid)

        if key == arcade.key.X:
            if self.NUM_ASTEROID !=0 :
                self.NUM_ASTEROID -= 1
                self.asteroids.pop()
                self.window.pop_asteroid()
                

    def update(self, delta):
        self.ship.update(delta)

        if self.ship.hit(self.gold, 40):
            self.gold.random_location()
            self.score += 1
        
        for asteroid in self.asteroids:
            asteroid.animate(delta)
            if self.ship.hit(asteroid, 10):
                self.score -= 1
                asteroid.x = 0
                asteroid.y = 0
                asteroid.random_direction()

class Gold(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
    def random_location(self):
        self.x = randint(0, self.world.width - 1)
        self.y = randint(0, self.world.height - 1)