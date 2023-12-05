import speech_recognition as sr
import numpy as np
import sounddevice as sd
import wave
import os
import pyttsx3


class Transcribir:
    def __init__(self, canales: int, tasa_muestreo: int, tamanio_bufer: int, duracion_grabacion: int, ruta_archivo: str):
        self.canales = canales
        self.tasa_muestreo = tasa_muestreo
        self.tamanio_bufer = tamanio_bufer
        self.duracion_grabacion = duracion_grabacion
        self.ruta_archivo = ruta_archivo

    def grabacion_de_audio(self):
        # si existe archivo de audio, borrarlo
        if os.path.exists('audio_grabacion.wav'):
            os.remove('audio_grabacion.wav')
        try:
            print("Grabando...")
            audio_data = sd.rec(int(self.tasa_muestreo * self.duracion_grabacion),
                                samplerate=self.tasa_muestreo, channels=self.canales, dtype=np.int16)
            sd.wait()

            print("Grabacion finalizada.")

            # Guardar el archivo de audio
            wf = wave.open(self.ruta_archivo, 'wb')
            wf.setnchannels(self.canales)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(self.tasa_muestreo)
            wf.writeframes(audio_data.tobytes())
            wf.close()

            resultado = self.transcribir_audio(self.ruta_archivo)

            return resultado

        except Exception as exception:
            raise NameError(f"Error al grabar el audio: {exception}")

    def transcribir_audio(self, ruta_audio):
        try:
            r = sr.Recognizer()
            audio_file = sr.AudioFile(ruta_audio)

            with audio_file as source:
                audio = r.record(source)

            texto = r.recognize_google(audio, language='es-ES')

            return texto

        except Exception as exception:
            raise NameError(f"Error al transcribir el audio: {exception}")
