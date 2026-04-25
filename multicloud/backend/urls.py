from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('resultados/',views.resultado, name = 'resultados'),
    path('detalle/<int:id>/', views.detalle, name = 'detalle'),
    path('api/login/', views.login_api, name = 'loginapi'),
    path('api/resultados/', views.resultados_api, name = 'resultadosapi'),
    path('api/detalle/<int:id>/', views.detalle_api, name = 'detalleapi'),
]