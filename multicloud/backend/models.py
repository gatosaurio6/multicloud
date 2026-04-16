from django.db import models
from django.core.validators import FileExtensionValidator, MinLengthValidator, RegexValidator

# Create your models here.

class Paciente (models.Model):
    nombre = models.CharField(max_length = 100)
    rut = models.CharField(max_length = 10, validators= [MinLengthValidator(9), RegexValidator(regex=r'^\d{7,8}-[0-9kK]$', message='El RUT debe tener el formato 12345678-K (con guion y sin puntos)')])
    correo = models.EmailField(unique = True)
    password = models.CharField(max_length = 255)

class Medico (models.Model):
    nombre = models.CharField(max_length = 100)
    rut = models.CharField(max_length = 10, validators= [MinLengthValidator(9), RegexValidator(regex=r'^\d{7,8}-[0-9kK]$', message='El RUT debe tener el formato 12345678-K (con guion y sin puntos)')])
    correo = models.EmailField(unique = True)

class Resultado (models.Model):
    paciente = models.ForeignKey(Paciente, on_delete = models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete = models.CASCADE)
    examen = models.CharField(max_length = 100)
    resultado = models.FileField(upload_to='documentos/')
    informe = models.FileField(upload_to='informes/', null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)