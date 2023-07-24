# constants.py
import pygame
from utils.buttonProperties import ButtonProperties
from utils.buttonTimerProperties import ButtonTimerProperties


BUTTON_SOUND_PROPERTIES = {
    "Bouton 1": ButtonProperties("a", 60, "assets/sounds/drum/BD_Tek_AHeat_1_1.wav"),
    "Bouton 2": ButtonProperties("b", 61, "assets/sounds/drum/Clap_Tek_AHeat_001.wav"),
    "Bouton 3": ButtonProperties("c", 62, "assets/sounds/drum/Conga_Tek_AHeat_1_1.wav"),
    # Ajoutez d'autres boutons et touches de clavier ici
}

BUTTON_TIMER_PROPERTIES = {
    "Bouton 4": ButtonTimerProperties(pygame.K_z, "START"),
    "Bouton 5": ButtonTimerProperties(pygame.K_e, "PAUSE"),
    "Bouton 6": ButtonTimerProperties(pygame.K_r, "STOP"),
    # Ajoutez d'autres boutons et touches de clavier ici
}

sound_tempo_1 = "assets/sounds/drum/HH_Tek_AHeat_1_1.wav"
sound_tempo_2 = "assets/sounds/drum/HH_Tek_AHeat_1_1.wav"

sound_tempo_3 = "assets/sounds/drum/BD_Tek_AHeat_1_1.wav"

stream = None
audio = None