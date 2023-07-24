import threading
import time

import pygame
from utils import constants


class Timer:
    def __init__(self, tempo):
        self.tempo = tempo
        self.sound_tempo_1 = constants.sound_tempo_1
        self.sound_tempo_2 = constants.sound_tempo_2
        self.is_starting = False
        self.nb_time = 0
        self.beat = 0
        self.play_beat_1 = pygame.mixer.Sound(constants.sound_tempo_1)
        self.play_beat_2 = pygame.mixer.Sound(constants.sound_tempo_2)
        self.thread_beat = None

    def start(self):
        if not self.is_starting:
            self.is_starting = True
            print("start")
            self.thread_beat = threading.Thread(target=self.beat_measure)
            self.thread_beat.start()


    def resume(self):
        if self.is_starting:
            self.is_starting = False
            print("Pause")
        else:
            self.is_starting = True
            print("unPause")

    def stop(self):
        if self.is_starting:
            self.is_starting = False
            self.nb_time = 0
            self.thread_beat.join()
        print("Stop")

    def restart(self):
        self.stop()
        self.start()

    def get_is_starting(self):
        return self.is_starting

    def beat_measure(self):
        while self.is_starting:
            time.sleep(self.tempo)
            self.nb_time = self.nb_time + 1
            self.beat = self.beat + 1
            if self.beat < 4:
                print("bip")
                self.play_beat_1.play()
            else:
                print("bop")
                self.beat = 0
                self.play_beat_2.play()

