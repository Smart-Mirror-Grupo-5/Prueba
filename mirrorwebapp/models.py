from django.db import models


class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=100)


class DatosPersona(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=20)
    habitacion = models.CharField(max_length=20)
    horario_med = models.CharField(max_length=20, choices=[
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ])
    problemas_medicos = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    medicamentos = models.TextField(blank=True, null=True)
    persona_contacto = models.CharField(max_length=100)
    telefono_contacto = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'
