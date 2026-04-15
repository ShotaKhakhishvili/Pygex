from ..Game import *
from ..Game.managers import cursor_manager
from .. import Game as GameModule

class UHUD(UBoxComponent):
    def __init__(self, color, width, height, classname = "UHUD"):
        super().__init__(color, width, height, classname)
        self.anchor = (0.0,0.0)
        self.center = (0.0,0.0)
        self.rect.x = self.anchor[0] * GameModule.screen_dims[0] - self.center[0] * self.rect.size[0] + self.get_world_pos()[0]
        self.rect.y = self.anchor[1] * GameModule.screen_dims[1] - self.center[1] * self.rect.size[1] + self.get_world_pos()[1]

    def update_shape(self):
        self.rect.x = self.anchor[0] * GameModule.screen_dims[0] - self.center[0] * self.rect.size[0] + self.get_world_pos()[0]
        self.rect.y = self.anchor[1] * GameModule.screen_dims[1] - self.center[1] * self.rect.size[1] + self.get_world_pos()[1]
        self.rect.width = self.width
        self.rect.height = self.height

class UButton(UHUD):
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


class UText(UPrimitiveComponent):
    def __init__(
        self,
        text,
        color,
        font_size=32,
        font_name=None,
        antialias=True,
        classname="Text",
    ):
        super().__init__(classname)

        self.text = text
        self.color = color
        self.font_size = font_size
        self.font_name = font_name
        self.antialias = antialias

        self.anchor = (0.0, 0.0)
        self.center = (0.0, 0.0)

        self._font = pygame.font.SysFont(self.font_name, self.font_size)
        self._surface = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self._render_text()
        self.update_shape()

    def _to_rgb(self):
        return self.color.red(), self.color.green(), self.color.blue()

    def _render_text(self):
        self._surface = self._font.render(str(self.text), self.antialias, self._to_rgb())
        self.rect.width, self.rect.height = self._surface.get_size()

    def update_shape(self):
        self.rect.x = int(
            self.anchor[0] * GameModule.screen_dims[0]
            - self.center[0] * self.rect.width
            + self.get_world_pos()[0]
        )
        self.rect.y = int(
            self.anchor[1] * GameModule.screen_dims[1]
            - self.center[1] * self.rect.height
            + self.get_world_pos()[1]
        )

    def _draw(self, screen):
        super()._draw(screen)
        self.update_shape()
        screen.blit(self._surface, self.rect)

    def set_text(self, text):
        self.text = text
        self._render_text()

    def set_font_size(self, font_size):
        self.font_size = font_size
        self._font = pygame.font.SysFont(self.font_name, self.font_size)
        self._render_text()

    def set_font_name(self, font_name):
        self.font_name = font_name
        self._font = pygame.font.SysFont(self.font_name, self.font_size)
        self._render_text()

    def set_antialias(self, antialias):
        self.antialias = antialias
        self._render_text()

    def set_color(self, color):
        self.color = color
        self._render_text()
