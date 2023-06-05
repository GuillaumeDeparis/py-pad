from pydub import AudioSegment
from pathlib import Path
import simpleaudio as sa
from pydub.playback import play

file_path = "resources/samples/drum/BD_Tek_AHeat_1_1.wav"

wav_path = Path(file_path)
wav_audio = AudioSegment.from_file(wav_path)
play(wav_audio)
