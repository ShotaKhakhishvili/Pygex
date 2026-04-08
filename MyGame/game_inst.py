from gamepackage.Game import Game, Color, InputType, AActor
from MainMenu import UMainMenu

class MyGame(Game):
    def update(self, dt):
        super().update(dt)

    def input_received(self, input_type : InputType):
        if input_type == InputType.QUIT:
            self.quit()

    def __init__ (self, screen_width, screen_height, color : Color):
        super().__init__(screen_width, screen_height, color)

        self.HUD = self.spawn_actor(AActor())

        self.main_menu = self.HUD.add_component(UMainMenu())

game = MyGame(800, 600, Color(20, 30, 50))
game.run()