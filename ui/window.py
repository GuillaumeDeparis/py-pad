import pygame
from ui.buttons import Button
from utils.timer import Timer

import utils.helpers as h


class Window:
    def __init__(self, width, height, audio):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Application Audio")
        self.audio = audio

        self.buttons = []  # Liste pour stocker les boutons
        self.timer = Timer(h.transform_time_to_tempo(120))

    def update(self):
        pygame.display.update()

    def fill(self, color):
        self.window.fill(color)

    def draw_text(self, text, position, color, font_size=20, font_name=None):
        font = pygame.font.Font(font_name, font_size) if font_name else pygame.font.SysFont(None, font_size)
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, position)

    def draw_button(self, rect, color, text, text_color, font_size=20, font_name=None):
        button = Button(self, rect, color, text, text_color, font_size, font_name)
        self.buttons.append(button)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.window)

    def add_button(self, button):
        self.buttons.append(button)

    def clear(self):
        self.fill((0, 0, 0))

    def handle_event(self, event):
        for button in self.buttons:
            # button.handle_event(event)
            button.check_key_press(event)
