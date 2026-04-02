from ..Game import *

class Button(Object):
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.is_hovered = False
        self.is_clicked = False
        self.is_pressed = False

        self.__button = pygame.Rect(x, y, width, height)

    def set_color(self, red, green, blue):
        self.color = Color(red, green, blue)

    def _draw(self, screen):
        pygame.draw.rect(screen, (  self.color.red(),
                                    self.color.green(), self.color.blue()),
                                    self.__button
                                    )

    def update(self):
        old_pressed = self.is_pressed
        old_hovered = self.is_hovered

        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.__button.collidepoint(mouse_pos)

        mouse_buttons = pygame.mouse.get_pressed()
        self.is_pressed = (mouse_buttons[0] and self.is_hovered) or (old_pressed and mouse_buttons[0])

        self.is_clicked = False

        if self.is_hovered:
            self.on_hovered()
            if not old_hovered:
                self.on_just_hovered()
        else:
            self.on_unhovered()
            if old_hovered:
                self.on_just_unhovered()

        if self.is_pressed:
            self.on_pressed()
            if not old_pressed:
                self.on_just_pressed()
        elif old_pressed:
            self.on_released()
            if self.is_hovered:
                self.is_clicked = True

    def on_just_hovered(self):
        pass
    def on_hovered(self):
        pass
    def on_just_unhovered(self):
        pass
    def on_unhovered(self):
        pass

    def on_just_pressed(self):
        pass
    def on_pressed(self):
        pass
    def on_released(self):
        pass