# estoque/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rota da página de upload
    path('upload-nfe/', views.upload_nfe_view, name='upload_nfe'),
    
    # Rota da página de saída de material
    path('saida-material/', views.saida_material_view, name='saida_material'),
    
    # Rota para a página de requisição
    path('criar-requisicao/', views.criar_requisicao_view, name='criar_requisicao'),

    # Rota para o Dashboard, com o nome 'dashboard'
    path('dashboard/', views.dashboard_view, name='dashboard'),
]