import pvrecorder
from pvrecorder import PvRecorder
import os
import wave
import numpy as np
import struct
import time
import speech_recognition as sr




class Transcripcion:
    def grabar(self):
        # (32 milliseconds of 16 kHz audio)
        recorder = PvRecorder(device_index=-1, frame_length=512)
        audio = []
        path = 'audio_recording.wav'
        duration = 6

        try:
            recorder.start()

            start_time = time.time()  # Marcar el tiempo de inicio

            while time.time() - start_time < duration:
                frame = recorder.read()
                audio.extend(frame)

            # Detener la grabación y guardarla en el archivo especificado
            recorder.stop()
            with wave.open(path, 'w') as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))
            recorder.delete()

        except Exception as exception:
            raise NameError(f"Error al grabar el audio: {exception}")

    def trascribir(self):
        try:
            r = sr.Recognizer()
            audio_file = sr.AudioFile('audio_recording.wav')

            with audio_file as source:
                audio = r.record(source)

            texto = r.recognize_google(audio, language='es-ES')

            return texto

        except Exception as exception:
            raise NameError(f"Error al transcribir el audio: {exception}")



"""class Transcribir:
    def __init__(self, device_index, frame_length, duration, file_path):
        self.device_index = device_index
        self.frame_length = frame_length
        self.duration = duration
        self.file_path = file_path

    def grabacion_de_audio(self):
        recorder = PvRecorder(
            # (32 milliseconds of 16 kHz audio)
            self.device_index, self.frame_length)
        audio = []
        path = self.file_path
        try:
            recorder.start()

            start_time = time.time()  # Marcar el tiempo de inicio

            while time.time() - start_time < self.duration:
                frame = recorder.read()
                audio.extend(frame)

            # Detener la grabación y guardarla en el archivo especificado
            recorder.stop()
            with wave.open(path, 'w') as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(audio), *audio))
            recorder.delete()

        except Exception as exception:
            raise NameError(f"Error al grabar el audio: {exception}")

        recognizer = sr.Recognizer()

        with sr.AudioFile(self.file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='es-ES')

        return text

    def transcribir_audio(self, ruta_audio):
        try:
            r = sr.Recognizer()
            audio_file = sr.AudioFile(ruta_audio)

            with audio_file as source:
                audio = r.record(source)

            texto = r.recognize_google(audio, language='es-ES')

            return texto

        except Exception as exception:
            raise NameError(f"Error al transcribir el audio: {exception}")"""