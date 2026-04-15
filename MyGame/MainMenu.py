from gamepackage.Game import UPrimitiveComponent, Color
from gamepackage.UI import UButton, UText
from gamepackage import Game as GamePackage
import pygame


class UMainMenu(UPrimitiveComponent):
    def __init__(self, classname = "UMainMenu"):
        super().__init__(classname)

        self.play = UButton(Color(200, 200, 200), 300, 100)
        self.play.center = (0.5, 0.5)
        self.play.anchor = (0.5, 0.5)
        self.play.pos = (0, 0)

        self.playText = UText("Play", Color(255, 255, 255), 56)
        self.playText.center = (0.5, 0.5)
        self.playText.anchor = (0.5, 0.5)
        self.playText.pos = (0, 0)

        self.quit = UQuitButton(Color(175, 30, 30), 150, 50)
        self.quit.center = (0.5, 0.5)
        self.quit.anchor = (0.5, 0.7)
        self.quit.pos = (0, 0)

        self.quitText = UText("Exit", Color(255, 255, 255))
        self.quitText.center = (0.5, 0.5)
        self.quitText.anchor = (0.5, 0.7)
        self.quitText.pos = (0, 0)

        self.add_child(self.play)
        self.add_child(self.playText)
        self.add_child(self.quit)
        self.add_child(self.quitText)

    def _draw(self, screen):
        self.play._draw(screen)
        self.quit._draw(screen)
        self.playText._draw(screen)
        self.quitText._draw(screen)

class UQuitButton(UButton):
    def on_pressed(self):
        GamePackage.Game.quit()