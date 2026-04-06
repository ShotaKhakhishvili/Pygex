from ..Game import *

class Button(UPrimitiveComponent):
    def __init__(self, width, height, color, classname="Button"):
        super().__init__(classname)

        self.width = width
        self.height = height
        self.color = color

        self.is_hovered = False
        self.is_clicked = False
        self.is_pressed = False

        self.rect = pygame.Rect(self.pos[0], self.pos[1], width, height)

    def update_rect(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.rect.width = self.width
        self.rect.height = self.height

    def set_color(self, red, green, blue):
        self.color = Color(red, green, blue)

    def _draw(self, screen):
        self.update_rect()
        pygame.draw.rect(screen, (  self.color.red(),
                                    self.color.green(), self.color.blue()),
                                    self.rect
                                    )

    def tick(self, dt):
        self.update_rect()
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