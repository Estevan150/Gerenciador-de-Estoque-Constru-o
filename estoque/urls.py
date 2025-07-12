# estoque/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rotas que já existiam
    path('upload-nfe/', views.upload_nfe_view, name='upload_nfe'),
    path('saida-material/', views.saida_material_view, name='saida_material'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('criar-requisicao/', views.criar_requisicao_view, name='criar_requisicao'),
]