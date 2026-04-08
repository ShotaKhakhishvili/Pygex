from __future__ import annotations

import pygame
from enum import Enum, auto

class InputType(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    QUIT = auto()


class Color:

    def __init__(self, red : int, green : int, blue : int):
        self.__red = red
        self.__green = green
        self.__blue = blue

    def __mul__(self, scale):
        return Color(
            self.__red * scale,
            self.__green * scale,
            self.__blue * scale
        )

    def red(self):
        return self.__red % 256
    def green(self):
        return self.__green % 256
    def blue(self):
        return self.__blue % 256

    def set_color(self, red, green, blue):
        self.__red = red
        self.__green = green
        self.__blue = blue

    def to_tuple(self):
        return self.red(), self.green(), self.blue()

class Renderer:
    def __init__(self, clear_color : Color):
        self._clear_color = Color(clear_color.red(), clear_color.green(), clear_color.blue())

    def draw(self, screen, objects : list):
        screen.fill(self._clear_color.to_tuple())

        for current_object in objects:
            current_object._draw(screen)

        pygame.display.flip()

class Game:
    def quit(self):
        self.__run = False
        pygame.quit()

    def update(self, dt):
        self.__check_for_inputs()
        self.__world.update(dt)

        self.__renderer.draw(self.__screen, self.__world.gather_render_primitives())

        self.__frame += 1

    def __init__(self, width : int, height : int, clear_color : Color):
        self.__run = True
        self.__frame = 0

        self.__width = width
        self.__height = height

        self.__clock = pygame.time.Clock()

        pygame.init()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.flip()

        self.__renderer = Renderer(clear_color)
        self.__world = World()

    def run(self):
        while self.__run:
            dt = self.__clock.tick(60) / 1000.0

            self.update(dt)

    def input_received(self, input_type : InputType):
        pass

    def __check_for_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.input_received(InputType.QUIT)
                continue

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.input_received(InputType.UP)
                    case pygame.K_DOWN:
                        self.input_received(InputType.DOWN)
                    case pygame.K_LEFT:
                        self.input_received(InputType.LEFT)
                    case pygame.K_RIGHT:
                        self.input_received(InputType.RIGHT)
                    case pygame.K_ESCAPE:
                        self.input_received(InputType.QUIT)

    def spawn_actor(self, obj : AActor):
        self.__world._register(obj)

        return obj
    def destroy_actor(self, obj : AActor):
        self.__world._unregister(obj)

class UObject:
    _internal_count = 0
    def __init__(self, classname="UObject"):
        UObject._internal_count += 1

        self.name = classname + str(UObject._internal_count)

class UActorComponent(UObject):
    def __init__(self, classname="UActorComponent"):
        super().__init__(classname)
        self._owner = None

    def set_owner(self, owner: "AActor"):
        self._owner = owner

    def get_owner(self):
        return self._owner

    def begin_play(self):
        pass

    def tick(self, dt):
        pass

    def on_destroy(self):
        pass

class USceneComponent(UActorComponent):
    def __init__(self, classname="USceneComponent"):
        super().__init__(classname)

        self.pos = (0, 0)
        self.rot = 0
        self.scale = (1, 1, 1)

        self.parent = None
        self.children = []

    def is_descendant_of(self, other):
        current = self.parent
        while current is not None:
            if current == other:
                return True
            current = current.parent
        return False

    def can_attach_to(self, new_parent):
        if new_parent is None:
            return True
        if new_parent == self:
            return False
        if new_parent.is_descendant_of(self):
            return False
        return True

    def set_parent(self, new_parent):
        if not self.can_attach_to(new_parent):
            print("CYCLIC PARENT-CHILD BEHAVIOUR DETECTED!")
            return

        if self.parent is not None:
            if self in self.parent.children:
                self.parent.children.remove(self)

        self.parent = new_parent

        if new_parent is not None:
            if self not in new_parent.children:
                new_parent.children.append(self)

    def add_child(self, child):
        if child is None:
            return
        child.set_parent(self)

    def remove_child(self, child):
        if child is None:
            return
        if child in self.children:
            self.children.remove(child)
            if child.parent == self:
                child.parent = None

    def get_world_pos(self):
        if self.parent is None:
            return self.pos
        px, py, pz = self.parent.get_world_pos()
        x, y = self.pos
        return px + x, py + y

class UPrimitiveComponent(USceneComponent):
    def __init__(self, classname="UPrimitiveComponent"):
        super().__init__(classname)

        self.visible = True
        self.z_order = 0

    def _draw(self, screen):
        pass

class UShapeComponent(UPrimitiveComponent):
    def __init__(self, color : Color, classname="UShapeComponent"):
        super().__init__(classname)
        self.color = color
        pass

    def set_color(self, red, green, blue):
        self.color = Color(red, green, blue)

    def get_scaled_shape(self):
        pass

    def get_shape_bounds(self):
        pass

    def update_shape(self):
        pass

class UBoxComponent(UShapeComponent):
    def __init__(self, color : Color, width, height, classname="UBoxComponent"):
        super().__init__(color, classname)

        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.pos[0], self.pos[1], width, height)

    def _draw(self, screen):
        self.update_shape()
        pygame.draw.rect(screen, (  self.color.red(),
                                    self.color.green(), self.color.blue()),
                                    self.rect
                                    )

    def update_shape(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.rect.width = self.width
        self.rect.height = self.height


class AActor(UObject):

    def __init__(self, classname="AActor"):
        super().__init__(classname)
        self._root = USceneComponent()
        self._root.set_owner(self)
        self._components = [self._root]

    def begin_play(self):
        pass

    def tick(self, dt):
        for component in self._components:
            component.tick(dt)
        pass

    def add_component(self, component: UActorComponent):
        if component is None:
            return

        component.set_owner(self)
        self._components.append(component)

        if isinstance(component, USceneComponent) and component.parent is None:
            component.set_parent(self._root)

        return component

    def get_components(self):
        return self._components

class World:
    def actors(self):
        return self.__registered_objects

    def __init__(self):
        self.__registered_objects = []
        self.__register_queue = []
        self.__unregister_queue = []

    def _register(self, obj):
        self.__register_queue.append(obj)

    def _unregister(self, obj):
        self.__unregister_queue.append(obj)

    def gather_render_primitives(self):
        primitives = []

        for actor in self.__registered_objects:
            if actor is None:
                continue

            for component in actor.get_components():
                if isinstance(component, UPrimitiveComponent) and component.visible:
                    primitives.append(component)

        primitives.sort(key=lambda primitive: primitive.z_order)
        return primitives

    def update(self, dt):
        for obj in self.__registered_objects:
            obj.tick(dt)

        for obj in self.__unregister_queue:
            if obj in self.__registered_objects:
                self.__registered_objects.remove(obj)

        for obj in self.__register_queue:
            if obj not in self.__registered_objects:
                self.__registered_objects.append(obj)
                obj.begin_play()

        self.__unregister_queue.clear()
        self.__register_queue.clear()
