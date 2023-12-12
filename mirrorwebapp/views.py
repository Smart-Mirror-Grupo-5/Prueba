# mirrorwebapp/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import DatosPersona
from .respuestas import consulta
from django.views.decorators.csrf import csrf_exempt
import azure.cognitiveservices.speech as speechsdk
from bs4 import BeautifulSoup
import requests
import speech_recognition as sr


@csrf_exempt
def reconocer_voz(request):
    if request.method == 'POST':
        SPEECH_KEY = '3c6987d5f8264f6eafe7d3eb9929e5f8'
        SPEECH_REGION = 'westeurope'

        speech_config = speechsdk.SpeechConfig(
            subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_recognition_language = "es-ES"

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config)

        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            resultado = speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            resultado = "No se pudo reconocer ningún discurso."
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            resultado = f"Reconocimiento de voz cancelado: {
                speech_recognition_result.cancellation_details.error_details}"
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
