import time
import tkinter as tk
import rtmidi
import mido
import pygame
import utils.constants


# Création de l'objet self.midiout


class MidiPad:
    def __init__(self):
        # self.midiout = rtmidi.MidiOut()
        self.midoOut = mido.open_output('loopMIDI Port 1')
        # Création de la fenêtre principale
        self.window = tk.Tk()
        self.window.title("Pad MIDI")
        self.sound = None
        self.start_time = 0
        self.end_time = 0

        pygame.mixer.init()

        # Création des boutons du pad MIDI
        self.buttons = [
            {"text": "Button 1", "note": 60, "key": "a", "type": "note",
             "sound": "C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/BD_Tek_AHeat_1_1.wav"},
            {"text": "Button 2", "note": 62, "key": "z", "type": "note",
             "sound": "C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/Clap_Tek_AHeat_019.wav"},
            {"text": "Button 3", "note": 64, "key": "e", "type": "note",
             "sound": "C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/Conga_Tek_AHeat_2_7.wav"},
            {"text": "Button 4", "note": 0, "key": "r", "type": "start",
             "sound": "C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/Conga_Tek_AHeat_2_7.wav"},
            {"text": "Button 5", "note": 0, "key": "t", "type": "stop",
             "sound": "C:/Users/guillaume.deparis/IdeaProjects/py-pad/assets/sounds/drum/Conga_Tek_AHeat_2_7.wav"}

            # Ajoutez d'autres boutons MIDI ici
        ]

        for button in self.buttons:
            btn = tk.Button(self.window, text=button["text"], width=10, height=3)
            btn.note = button["note"]  # Attribuez la note MIDI au bouton
            btn.bind("<ButtonPress> ", self.button_press)
            btn.bind("<ButtonRelease>", self.button_release)
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            btn.sound = pygame.mixer.Sound(button["sound"])
            btn.type = button["type"]

        self.window.bind_all("<KeyPress>", self.key_press)
        self.window.bind_all("<KeyRelease>", self.key_release)

        # Ouvrir le port MIDI
        # self.midiout.open_port(1)  # Modifier l'indice du port MIDI si nécessaire
        print("Ouverture du port")
        # Lancer la boucle principale de l'interface utilisateur
        self.window.mainloop()
        print("Fermeture du port")
        # Fermer le port MIDI lorsque la fenêtre est fermée
        del self.midoOut

    # Fonction pour envoyer un message "note on" MIDI
    def play_note_on(self, note):
        note_on = [0x90, note, 112]  # Vélocité fixée à 112
        note_on = mido.Message(type='note_on', note=note, velocity=64 , channel=0)
        self.midoOut.send(note_on)

    # Fonction pour envoyer un message "note off" MIDI
    def play_note_off(self, note):
        note_off = [0x80, note, 0]  # Vélocité à 0 pour arrêter la note
        note_off = mido.Message('note_off', note=note, velocity=64 , channel=0)
        self.midoOut.send(note_off)

    # Fonction appelée lorsqu'un bouton est pressé
    def button_press(self, event):
        self.start_time = time.time()
        print(self.start_time)
        note = event.widget.note
        if event.widget.type == "note":
            event.widget.sound.play()
            self.play_note_on(note)
        elif event.widget.type == "start":
            self.start_record()
        elif event.widget.type == "stop":
            self.stop_record()

    # Fonction appelée lorsqu'un bouton est relâché
    def button_release(self, event):
        note = event.widget.note
        self.end_time = time.time()
        print(self.end_time)
        self.play_note_off(note)

    def get_midi_out(self):
        return self.midiout

    def key_press(self, event):
        for btn in self.buttons:
            if btn["key"] == event.char:
                if btn["type"] == "note":
                    pygame.mixer.Sound(btn["sound"]).play()
                    self.play_note_on(btn["note"])
                elif btn["type"] == "start":
                    self.start_record()
                elif btn["type"] == "stop":
                    self.stop_record()

    def key_release(self, event):
        for btn in self.buttons:
            if btn["key"] == event.char:
                self.play_note_off(btn["note"])

    def start_record(self):
        message = mido.Message('start')
        self.start_time = time.time()
        self.midoOut.send(message)

    def stop_record(self):
        message = mido.Message('stop')
        self.start_time = 0
        self.midoOut.send(message)

    def continue_record(self):
        message = mido.Message('continue')
        self.midoOut.send(message)

    def reset_record(self):
        message = mido.Message('reset')
        self.midoOut.send(message)

    def clock(self):
        message = mido.Message('clock')
        self.midoOut.send(message)

    def clock(self):
        message = mido.Message('quarter_frame')
        self.midoOut.send(message)
