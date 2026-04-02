import pygame

class InputType:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    QUIT = 4


class Color:
    __red = 0
    __green = 0
    __blue = 0

    def __init__(self, red, green, blue):
        self.__red = red
        self.__green = green
        self.__blue = blue

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



class Renderer:
    __clear_color = Color(0,0,0)

    def __init__(self, clear_color : Color):
        self.__clear_color = Color(clear_color.red(), clear_color.green(), clear_color.blue())

    def draw(self, screen, objects : list):
        screen.fill((self.__clear_color.red(),
                    self.__clear_color.green(),
                    self.__clear_color.blue()))

        for current_object in objects:
            current_object._draw(screen)

        pygame.display.flip()

class Game:
    __run = True
    __frame = 0

    def quit(self):
        self.__run = False
        pygame.quit()

    def update(self):
        self.__renderer.draw(self.__screen, self.__world.registered_objects())

        self.__check_for_inputs()
        self.__world.update()

        self.__frame += 1

    def __init__(self, width : int, height : int, clear_color : Color):

        self.__width = width
        self.__height = height

        pygame.init()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.flip()

        self.__renderer = Renderer(clear_color)
        self.__world = self.__world = World(self.__renderer)

    def run(self):
        while self.__run:
            self.update()

    def input_received(self, input_type : InputType):
        pass

    def __check_for_inputs(self):
        for event in pygame.event.get():
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

    def create_object(self, obj : Object):
        self.__world._register(obj)
    def destroy_object(self, obj : Object):
        self.__world._unregister(obj)

class Object:
    def _draw(self, screen):
        pass

    def update(self):
        pass

class World:
    def registered_objects(self):
        return self.__registered_objects

    def __init__(self, renderer : Renderer):
        self.__registered_objects = []
        self.__register_queue = []
        self.__unregister_queue = []

        self.__renderer = renderer

    def _register(self, obj):
        self.__register_queue.append(obj)

    def _unregister(self, obj):
        self.__unregister_queue.append(obj)

    def _draw(self, screen):
        self.__renderer.draw(screen, self.__registered_objects)

    def update(self):
        for obj in self.__unregister_queue:
            self.__registered_objects.remove(obj)

        for obj in self.__register_queue:
            self.__registered_objects.append(obj)

        self.__unregister_queue.clear()
        self.__register_queue.clear()
