from django.shortcuts import render, redirect, get_object_or_404
from .models import Paciente, Resultado, Medico
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import check_password
import re
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def login (request):
    if request.method == "POST":
        correo = request.POST.get('correo').strip().lower()
        password = request.POST.get('password')
        try:
            paciente = Paciente.objects.get(correo = correo)
            if password == paciente.password:
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
    informes = Resultado.objects.filter(paciente_id=paciente_id, informe__isnull=False).select_related('medico').exclude(informe='')
    imagenes = Resultado.objects.filter(paciente_id=paciente_id, imagen__isnull=False).select_related('medico').exclude(imagen='')
    return render(request, 'resultados.html', {'informe': informes, 'imagen': imagenes})

#@requiere_login
def detalle(request, id):
    resultado = Resultado.objects.get(id=id)
    return render(request, 'detalle.html', {'resultado':resultado})

@csrf_exempt
def login_api(request):
    if request.method == "POST":
        correo = request.POST.get('correo','').strip().lower()
        password = request.POST.get('password', '').strip()

        try:
            paciente = Paciente.objects.get(correo = correo)

            if password == paciente.password:
                return JsonResponse({
                    "success":True,
                    "paciente_id": paciente.id,
                    "nombre": paciente.nombre
                })
            else:
                return JsonResponse({"success": False, "error": "credenciales incorrectas"})
        except Paciente.DoesNotExist:
            return JsonResponse({"success": False, "error": "credenciales incorrectas"})
    return JsonResponse({"error": "metodo no permitido"}, status = 405)

def resultados_api(request):
    paciente_id = request.GET.get('paciente_id')

    resultados = Resultado.objects.filter(paciente_id = paciente_id).select_related('medico')

    data = []

    for r in resultados:
        data.append({
            "id": r.id,
            "examen": r.examen,
            "medico": r.medico.nombre,
            "imagen": request.build_absolute_uri(r.imagen.url) if r.imagen else None,
            "informe": request.build_absolute_uri(r.informe.url) if r.informe else None,
        })
    return JsonResponse(data, safe=False)

def detalle_api(request, id):
    r = get_object_or_404(Resultado, id=id)

    data = {
        "id": r.id,
        "examen": r.examen,
        "medico": r.medico.nombre,
        "imagen": request.build_absolute_uri(r.imagen.url) if r.imagen else None,
        "informe": request.build_absolute_uri(r.informe.url) if r.informe else None,
    }

    return JsonResponse(data)


    
        
