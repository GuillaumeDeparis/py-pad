import pygame
from ui.midiPad import MidiPad
import threading
import mido
import time


class MidiStation:
    def __init__(self):
        self.__midoIn = mido.open_input(callback=self.midi_callback)
        self.__track = mido.MidiTrack()
        self.__midiFile = mido.MidiFile()
        self.__last_time = 0
        self.__actual_time = time.time()

        self.__start_record = False
        self.__nb_beat = 4
        self.__duration = 0
        self.__start_record_time = 0
        self.tempo = 100
        self.__measure = (60 / self.tempo) * self.__nb_beat
        self.__track.append(mido.MetaMessage('set_tempo', tempo=int(mido.tempo2bpm(self.tempo))))
        self.__track.append(mido.MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24,
                                             notated_32nd_notes_per_beat=16))

        recording_thread = threading.Thread(target=self.startMidiPad)
        recording_thread.start()

    @staticmethod
    def startMidiPad():
        pad = MidiPad()

    def midi_callback(self, event):
        if self.__start_record and self.__start_record_time != 0:
            self.__duration = time.time() - self.__start_record_time
            if self.__duration >= 5:
                self.stop_record()
                self.play_record()

        miditime = self.calcul_duration()
        if event.type in ['note_on', 'note_off']:
            print("S__start_record: ", self.__start_record)
            if self.__start_record:
                if self.__start_record_time == 0:  # permet de démarrer l'enregistrement
                    print("Declenchement du start record time")
                    self.__start_record_time = time.time()
                self.__track.append(mido.Message(event.type, note=event.note, velocity=event.velocity,
                                                 time=miditime))

        elif event.type == 'start':
            self.start_record()

        elif event.type == 'stop':
            self.stop_record()

        elif event.type == 'clock':
            print("Clock: ", event)

    def calcul_duration(self):
        if self.__last_time == 0:
            delay = 0
        else:
            delay = time.time() - self.__last_time
        self.__last_time = time.time()
        miditime = int(round(mido.second2tick(delay, self.__midiFile.ticks_per_beat, mido.bpm2tempo(self.tempo))))
        print("miditime: ", miditime)
        return miditime

    def snap_to_grid(self, time):
        # Identifier si il s'agît d'une noire en déduire le temps et coller la note au beat le plus proche
        print("Snap to grid")
        # Noire : quarter note +-5% sur sa durée
        # croche : height note +- 5% sur sa durée
        resolution = mido.tempo2bpm(self.tempo)

    def start_record(self):
        print("Start record")
        self.__start_record = True

    def stop_record(self):
        print("Stop record")
        self.__start_record = False
        self.__midiFile.tracks.append(self.__track)
        self.__midiFile.save("record.mid")

    def play_record(self):
        for msg in self.__midiFile.play():
            print(msg.time)
            time.sleep(msg.time)
            if not msg.is_meta or msg.type != 'program_change':
                if msg.type == 'note_on':
                    if msg.note == 60:
                        pygame.mixer.Sound(
                            'C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/BD_Tek_AHeat_1_1.wav').play()
                    elif msg.note == 62:
                        pygame.mixer.Sound(
                            'C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/Clap_Tek_AHeat_019.wav').play()
                    elif msg.note == 64:
                        pygame.mixer.Sound(
                            'C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/Conga_Tek_AHeat_2_7.wav').play()
