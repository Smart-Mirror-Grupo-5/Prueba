import pvrecorder as pv
import time
import struct

recorder = pv.PvRecorder(device_index=-1, frame_length=512, buffered_frames_count=50)
recorder.start()
duration = 6

audio = b''  # Initialize as bytes

start_time = time.time()  # Marcar el tiempo de inicio

while time.time() - start_time < duration:
    frame = recorder.read()
    audio += struct.pack("<" + "h" * len(frame), *frame)

recorder.stop()

print(audio)


import speech_recognition as sr

rec = sr.Recognizer()

# Convertir audio a texto
try:
    text = rec.recognize_google(audio, language='es-ES')  # Cambia el idioma según necesites
    print("Texto reconocido:")
    print(text)
except sr.UnknownValueError:
    print("No se pudo reconocer el audio")
except sr.RequestError as e:
    print(f"Error en la solicitud al servicio de reconocimiento de voz; {e}")
