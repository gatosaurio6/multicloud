from django.shortcuts import render, redirect, get_object_or_404
from .models import Paciente, Resultado, Medico
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import check_password
import re
from functools import wraps
# Create your views here.

def login (request):
    if request.method == "POST":
        correo = request.POST.get('correo').strip().lower()
        password = request.POST.get('password')
        try:
            paciente = Paciente.objects.get(correo = correo)
            if check_password(password, paciente.password):
                request.session['paciente_id'] = paciente.id
                request.session['nombre'] = paciente.nombre
                return redirect('resultados')
            else:
                messages.error(request, 'correo o contraseña incorrectos.')
        except Paciente.DoesNotExist:
            messages.error(request, 'correo o contraseña incorrectos.')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def requiere_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'paciente_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

#@requiere_login
def resultado(request):
    paciente_id = request.session.get('paciente_id')
    informes = Resultado.objects.filter(paciente_id=paciente_id, informe__isnull=False).select_related('medico')
    imagenes = Resultado.objects.filter(paciente_id=paciente_id, imagen__isnull=False).select_related('medico')
    return render(request, 'resultados.html', {'informe': informes, 'imagen': imagenes})

#@requiere_login
def detalle(request, id):
    resultado = Resultado.objects.get(id=id)
    return render(request, 'detalle.html', {'resultado':resultado})