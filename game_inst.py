from gamepackage.Game import Game, Color, InputType
from gamepackage.UI import Button

class MyGame(Game):
    def update(self):
        super().update()

    def input_received(self, input_type : InputType):
        if input_type == InputType.QUIT:
            self.quit()

    def __init__ (self, screen_width, screen_height, color : Color):
        super().__init__(screen_width, screen_height, color)

        self.create_object(Button(300, 300, 100, 50, Color(120, 50, 40)))

game = MyGame(800, 600, Color(20, 30, 50))
game.run()