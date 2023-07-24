import logging

import pygame
from utils import constants
from audio.player import Player
import wave
import time
import pyaudio


class Button:
    def __init__(self, window, rect, color, text, text_color, font_size=20, font_name=None):
        self.window = window
        self.rect = rect
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font_name = font_name
        self.clicked = False
        self.assigning_key = False
        self.wf = None

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        self.window.draw_text(self.text, (self.rect.x + self.rect.width // 2 - self.font_size // 2,
                                          self.rect.y + self.rect.height // 2 - self.font_size // 2),
                              self.text_color, self.font_size, self.font_name)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                print("Bouton cliqué :")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.assigned_key:
            print(f"Touche affectée pour le bouton '{self.text}' déclenchée")

    def get_assigned_key(self):
        button_name = self.text
        key_code = constants.BUTTON_KEY_BINDINGS.get(button_name)
        if key_code:
            return key_code
        else:
            print(f"Touche non définie pour le bouton '{button_name}'")
            return None


class PadButton(Button):
    def __init__(self, window, rect, color, text, text_color, font_size=20, font_name=None):
        super().__init__(window, rect, color, text, text_color, font_size, font_name)
        self.button_sound_properties = self.get_button_properties()

    def get_button_properties(self):
        button_name = self.text
        button_props = constants.BUTTON_SOUND_PROPERTIES.get(button_name)
        if button_props:
            return button_props
        else:
            logging.warning(f"Propriétés non définies pour le bouton '{button_name}'")
            return None

    @property
    def assigned_key(self):
        if self.button_sound_properties:
            return self.button_sound_properties.assigned_key
        else:
            return None

    @property
    def sound_to_play(self):
        if self.button_sound_properties:
            return self.button_sound_properties.sound_to_play
        else:
            return None

    def check_key_press(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.assigned_key:
            print(f"Touche affectée pour le bouton '{self.text}' déclenchée")
            self.play_sound()

    def _callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        # If len(data) is less than requested frame_count, PyAudio automatically
        # assumes the stream is finished, and the stream stops.
        return data, pyaudio.paContinue

    def play_sound(self):
        CHUNK = 1024
        with wave.open(self.sound_to_play, 'rb') as wf:
            self.wf = wf
            stream = self.window.audio.open(format=self.window.audio.get_format_from_width(wf.getsampwidth()),
                                            channels=wf.getnchannels(),
                                            rate=wf.getframerate(), output=True, stream_callback=self._callback)
            while stream.is_active():  # Requires Python 3.8+ for :=
                time.sleep(0.1)
            stream.close()
        ##sound = pygame.mixer.Sound(self.sound_to_play)
        ##sound.play()


class TimeButton(Button):
    def __init__(self, window, rect, color, text, text_color, font_size=20, font_name=None):
        super().__init__(window, rect, color, text, text_color, font_size, font_name)
        self.sound_tempo_1 = constants.sound_tempo_1
        self.sound_tempo_2 = constants.sound_tempo_2
        self.button_timer_properties = self.get_button_properties()
        self.player = Player()

    def get_button_properties(self):
        button_name = self.text
        button_props = constants.BUTTON_TIMER_PROPERTIES.get(button_name)
        if button_props:
            return button_props
        else:
            logging.warning(f"Propriétés non définies pour le bouton '{button_name}'")
            return None

    @property
    def assigned_key(self):
        if self.button_timer_properties:
            return self.button_timer_properties.assigned_key
        else:
            return None

    @property
    def function(self):
        if self.button_timer_properties:
            return self.button_timer_properties.function
        else:
            return None

    def check_key_press(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.assigned_key:
            if self.function == "START":
                print("Start timer")
                # create new thread
                self.window.timer.start()
                file_path = "output.wav"
                duration = 5
                # self.player.load_wav(file_path)
                self.player.start_recording()
                # self.player.record_played_audio(file_path, duration)

            elif self.function == "PAUSE":
                print("Pause timer")
                self.window.timer.resume()
            elif self.function == "STOP":
                print("Stop timer")
                self.window.timer.stop()
                self.player.stop_recording()

            print(f"Touche affectée pour le bouton '{self.text}' déclenchée")
            # self.sound_to_play.play()
