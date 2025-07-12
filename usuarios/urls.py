# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Ex: http://127.0.0.1:8000/usuarios/aprovar/TOKEN_VEM_AQUI/
    path('aprovar/<uuid:token>/', views.aprovar_usuario, name='aprovar_usuario'),
]