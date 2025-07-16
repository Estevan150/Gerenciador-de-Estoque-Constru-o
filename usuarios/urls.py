# usuarios/urls.py
from django.urls import path
# Importamos as views de autenticação prontas do Django
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Nossa URL de aprovação de usuário (já existia)
    path('aprovar/<uuid:token>/', views.aprovar_usuario, name='aprovar_usuario'),

    # --- NOSSAS NOVAS URLS DE LOGIN E LOGOUT ---

    # URL de Login:
    # Usamos a LoginView pronta do Django, mas dizemos a ela para usar o nosso template customizado.
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),

    # URL de Logout:
    # A LogoutView do Django já cuida de tudo para deslogar o usuário.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]