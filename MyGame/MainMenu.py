from gamepackage.Game import UPrimitiveComponent, Color
from gamepackage.UI import UButton


class UMainMenu(UPrimitiveComponent):
    def __init__(self, classname = "UMainMenu"):
        super().__init__(classname)

        self.play = UButton(Color(200, 200, 200), 300, 100)
        self.play.pos = (250, 250)

        self.add_child(self.play)

    def _draw(self, screen):
        self.play._draw(screen)