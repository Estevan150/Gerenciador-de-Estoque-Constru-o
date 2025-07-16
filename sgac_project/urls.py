# sgac_project/urls.py

from django.contrib import admin
from django.urls import path, include
from usuarios.views import custom_admin_login

# --- INÍCIO DA SOLUÇÃO (Importações necessárias) ---
from django.conf import settings
from django.conf.urls.static import static
# ----------------------------------------------------

urlpatterns = [
    path('admin/login/', custom_admin_login),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('estoque/', include('estoque.urls')),
]

# --- BLOCO FINAL ADICIONADO (A Mágica Acontece Aqui) ---
# Este 'if' garante que esta configuração de URL só seja usada
# quando DEBUG=True no seu settings.py.
if settings.DEBUG:
    # Adiciona uma rota especial para servir arquivos da sua STATIC_URL
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ---------------------------------------------------------