# mirrorwebapp/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import DatosPersona
from django.views.decorators.csrf import csrf_exempt
from .audio import Transcribir
import pyaudio


@csrf_exempt
def transcribir_audio(request):
    if request.method == 'POST':
        canales = 1
        tasa_muestreo = 44100
        tamanio_bufer = 512
        duracion_grabacion = 5
        ruta_archivo = 'static/audio/audio.wav'

        transcribir = Transcribir(
            canales, tasa_muestreo, tamanio_bufer, duracion_grabacion, ruta_archivo)

        recogida_audio = transcribir.grabacion_de_audio()

        # Devuelve la transcripción como JSON
        return JsonResponse({'transcripcion': recogida_audio})

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def entrar(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre')
        contraseña = request.POST.get('contraseña')

        if nombre_usuario == 'admin' and contraseña == 'admin':
            return redirect('espejo')

        error_message = "Credenciales incorrectas. Inténtalo de nuevo."
        return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def login(request):
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
