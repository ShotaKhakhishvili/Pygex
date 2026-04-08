import pygame

class CursorManager:
    def __init__(self):
        self.PRIORITIES = {
            pygame.SYSTEM_CURSOR_WAIT: 3,
            pygame.SYSTEM_CURSOR_IBEAM: 2,
            pygame.SYSTEM_CURSOR_HAND: 1,
            pygame.SYSTEM_CURSOR_ARROW: 0
        }
        self._requested_this_frame = pygame.SYSTEM_CURSOR_ARROW

    def request(self, cursor_type):
        current_prio = self.PRIORITIES.get(self._requested_this_frame, 0)
        new_prio = self.PRIORITIES.get(cursor_type, 0)

        if new_prio > current_prio:
            self._requested_this_frame = cursor_type

    def update(self):
        if pygame.mouse.get_cursor()[0] != self._requested_this_frame:
            pygame.mouse.set_cursor(self._requested_this_frame)

        self._requested_this_frame = pygame.SYSTEM_CURSOR_ARROW

cursor_manager = CursorManager()