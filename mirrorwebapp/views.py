# mirrorwebapp/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import DatosPersona
from .respuestas import consulta
from django.views.decorators.csrf import csrf_exempt
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, ResultReason
from bs4 import BeautifulSoup
import requests
import re
import wikipedia

def reconocer_voz(request):
    if request.method == 'POST':
        SPEECH_KEY = '3c6987d5f8264f6eafe7d3eb9929e5f8'
        SPEECH_REGION = 'westeurope'

        # Configuración de Azure Speech
        speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_recognition_language = "es-ES"

        # Configuración de audio para la transmisión
        audio_config = AudioConfig(use_default_microphone=False)

        # Configuración de reconocimiento de voz
        speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        # Inicia la transmisión de audio en tiempo real desde el servicio de Azure Speech
        stream = speech_recognizer.start_continuous_recognition()

        # Recolecta el texto a medida que se reconoce
        resultado = ""
        for phrase in stream:
            if phrase.reason == ResultReason.RecognizedSpeech:
                resultado += phrase.text
            elif phrase.reason == ResultReason.NoMatch:
                resultado = "No se pudo reconocer ningún discurso."
            elif phrase.reason == ResultReason.Canceled:
                resultado = f"Reconocimiento de voz cancelado: {phrase.cancellation_details.reason}"

        # Detén el reconocimiento continuo
        speech_recognizer.stop_continuous_recognition()

        contestacion = consulta(resultado)

        return JsonResponse({'resultado': resultado, 'contestacion': contestacion})

    return render(request, 'espejo.html')



def login(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre')
        contraseña = request.POST.get('contraseña')

        if nombre_usuario == 'admin' and contraseña == 'admin':
            return redirect('espejo')

        error_message = "Credenciales incorrectas. Inténtalo de nuevo."
        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def espejo(request):
    return render(request, 'espejo.html')


def añadirusuario(request):
    return render(request, 'añadirusuario.html')


def ayuda(request):
    return render(request, 'ayuda.html')


def habitacion(request):
    return render(request, 'habitacion.html')


def procesar_formulario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        fecha_nacimiento = request.POST.get('fechaNacimiento')
        dni = request.POST.get('dni')
        habitacion = request.POST.get('habitacion')
        horario_med = request.POST.get('horarioMed')
        problemas_medicos = request.POST.get('problemasMedicos')
        alergias = request.POST.get('alergias')
        medicamentos = request.POST.get('medicamentos')
        persona_contacto = request.POST.get('personaContacto')
        telefono_contacto = request.POST.get('telefonoContacto')

        # Guardar en la base de datos
        datos_persona = DatosPersona(
            nombre=nombre,
            apellidos=apellidos,
            fecha_nacimiento=fecha_nacimiento,
            dni=dni,
            habitacion=habitacion,
            horario_med=horario_med,
            problemas_medicos=problemas_medicos,
            alergias=alergias,
            medicamentos=medicamentos,
            persona_contacto=persona_contacto,
            telefono_contacto=telefono_contacto,
        )
        datos_persona.save()

        # Redirigir a alguna página de éxito o a donde desees después de guardar los datos
        return redirect('index')

    return render(request, 'añadirusuario.html')
