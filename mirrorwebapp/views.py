# mirrorwebapp/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import DatosPersona
from django.views.decorators.csrf import csrf_exempt
from .audio import Transcripcion
import io
import azure.cognitiveservices.speech as speechsdk

@csrf_exempt
def transcribir_audio(request):
    if request.method == 'POST':
        audio_blob = io.BytesIO(request.body)

        # Configurar el servicio de voz de Azure
        azure_key = '/F28MIc5gYxYYl9CuMEQASAd9cdfCyqrZk1ZIhXaaBibsH1/b6FwnMjnNYIiSUnXRZUUApB4RXLY7D/t88xtQg=='
        azure_endpoint = 'https://comunicacionespejito.europe.communication.azure.com/'
        speech_config = speechsdk.SpeechConfig(
            subscription=azure_key, endpoint=azure_endpoint)

        # Crear el reconocedor de voz con el audio proporcionado
        audio_config = speechsdk.audio.AudioConfig(stream=audio_blob)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config)

        # Realizar la transcripción
        result = recognizer.recognize_once()

        # Obtener el texto transcrito
        texto_transcrito = result.text

        # Devolver el texto transcrito como JSON
        return JsonResponse({'texto_transcrito': texto_transcrito})

    return JsonResponse({'error': 'Método no permitido'}, status=405)



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
