# Fichier contenant la classe responsable de la lecture des fichiers audio
import wave
import pyaudio

import numpy as np
from utils.constants import stream

class Player:
    def __init__(self):
        self.channels = 2
        self.audio_data = None
        self.devices = None
        self.duration = 5
        self.buffer = None
        self.sample_rate = 44100
        self.format = pyaudio.paInt16
        self.frames = []

        self.audio = pyaudio.PyAudio()

    def _callback(self, indata, frames, time, status):
        self.buffer = np.concatenate((self.buffer, indata))

    def start_recording(self):
        
        stream = self.audio.open(format=self.format, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=1024)
        #self.stream.stop_stream()
        print("Enregistrement en cours...")
        for _ in range(0, int(self.sample_rate / 4096 * self.duration)):
            data = stream.read(4096 )
            self.frames.append(data)

    def stop_recording(self):
        stream.stop_stream()
        self.audio.terminate()
        self.save_to_file()


    def save_to_file(self):
        wave_file = wave.open("output.wav", "wb")
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.audio.get_sample_size(format))
        wave_file.setframerate(self.sample_rate)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

