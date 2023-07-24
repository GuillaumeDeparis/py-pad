import time

import pygame
from ui.window import Window
from ui.buttons import PadButton, TimeButton
import pyaudio

pygame.init()
audio = pyaudio.PyAudio()
window = Window(400, 400, audio)

padButton1 = PadButton(window, pygame.Rect(100, 100, 100, 50), (255, 0, 0), "Bouton 1", (255, 255, 255))
padButton2 = PadButton(window, pygame.Rect(100, 200, 100, 50), (0, 255, 0), "Bouton 2", (255, 255, 255))
padButton3 = PadButton(window, pygame.Rect(100, 300, 100, 50), (0, 0, 255), "Bouton 3", (255, 255, 255))

startButton = TimeButton(window, pygame.Rect(100, 100, 100, 50), (255, 0, 0), "Bouton 4", (255, 255, 255))
pauseButton = TimeButton(window, pygame.Rect(100, 100, 100, 50), (255, 0, 0), "Bouton 5", (255, 255, 255))
StopButton = TimeButton(window, pygame.Rect(100, 100, 100, 50), (255, 0, 0), "Bouton 6", (255, 255, 255))

window.add_button(padButton1)
window.add_button(padButton2)
window.add_button(padButton3)
window.add_button(startButton)
window.add_button(pauseButton)
window.add_button(StopButton)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Gestion des événements des boutons
        window.handle_event(event)
    window.clear()  # Effacer l'écran

    # Dessiner les boutons
    window.draw_buttons()

    pygame.display.flip()
pyaudio.terminate()
pygame.quit()
