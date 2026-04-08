from ..Game import *
from ..Game.managers import cursor_manager


class UButton(UBoxComponent):
    def __init__(self, color, width, height, classname="Button"):
        super().__init__(color, width, height, classname)

        self.color_hovered = color * 0.9
        self.color_pressed = color * 0.75
        self.default_color = color

        self.is_hovered = False
        self.is_clicked = False
        self.is_pressed = False

    def update_shape(self):
        super().update_shape()
        if self.is_pressed:
            self.color = self.color_pressed
            cursor_manager.request(pygame.SYSTEM_CURSOR_HAND)
        elif self.is_hovered:
            self.color = self.color_hovered
            cursor_manager.request(pygame.SYSTEM_CURSOR_SIZEALL)
        else:
            self.color = self.default_color
            cursor_manager.request(pygame.SYSTEM_CURSOR_ARROW)

    def tick(self, dt):
        super().tick(dt)

        self.update_shape()
        old_pressed = self.is_pressed
        old_hovered = self.is_hovered

        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        mouse_buttons = pygame.mouse.get_pressed()
        self.is_pressed = mouse_buttons[0] and (self.is_hovered or old_pressed)

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
                self.on_clicked()

        if self.is_pressed:
            cursor_manager.request(pygame.SYSTEM_CURSOR_HAND)
        elif self.is_hovered:
            cursor_manager.request(pygame.SYSTEM_CURSOR_HAND)
        else:
            cursor_manager.request(pygame.SYSTEM_CURSOR_ARROW)

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

    def on_clicked(self):
        pass