import arcade
from models import Ship,World

 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def draw(self):
        self.sync_with_model()
        super().draw()

class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(self, width, height)        # แทนที่บรรทัด ship
        self.ship_sprite = ModelSprite('images/ship.png',model=self.world.ship)
        self.gold_sprite = ModelSprite('images/gold.png',model=self.world.gold)
        self.asteroid_sprites = []
        for asteroid in self.world.asteroids:
            self.asteroid_sprites.append(ModelSprite('images/ship.png',scale=0.5,model=asteroid))

    def on_draw(self):
        arcade.start_render()
        self.gold_sprite.draw()
        self.ship_sprite.draw()

        for sprite in self.asteroid_sprites:
            sprite.draw()

        arcade.draw_text(str(self.world.NUM_ASTEROID),
                        self.width - 60, self.height - 30,
                        arcade.color.WHITE, 20)
 
    def update(self, delta):
        self.world.update(delta)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def insert_asteroid(self, x):
        self.asteroid_sprites.append(ModelSprite('images/ship.png',scale=0.5,model=x))
    def pop_asteroid(self):
        self.asteroid_sprites.pop()

if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
    