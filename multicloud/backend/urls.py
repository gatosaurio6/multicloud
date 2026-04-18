from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('resultados/',views.resultado, name = 'resultados'),
    path('detalle/<int:id>/', views.detalle, name = 'detalle'),
]