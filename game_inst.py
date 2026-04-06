from gamepackage.Game import Game, Color, InputType, AActor
from gamepackage.UI import Button

class MyGame(Game):
    def update(self, dt):
        super().update(dt)

    def input_received(self, input_type : InputType):
        if input_type == InputType.QUIT:
            self.quit()

    def __init__ (self, screen_width, screen_height, color : Color):
        super().__init__(screen_width, screen_height, color)

        HUD = self.spawn_actor(AActor())

        button = HUD.add_component(Button(300, 300, Color(120, 50, 40)))

        button.pos = (50, 50)



game = MyGame(800, 600, Color(20, 30, 50))
game.run()